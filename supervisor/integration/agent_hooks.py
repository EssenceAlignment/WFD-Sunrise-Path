#!/usr/bin/env python3
"""
Agent Integration Hooks for Cascade Governor
Inserts admission control into existing cascade scripts
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional
from functools import wraps

GOVERNOR_URL = "http://localhost:8080"

class GovernorClient:
    """Client for interacting with Cascade Governor"""

    def __init__(self, base_url: str = GOVERNOR_URL):
        self.base_url = base_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def request_permission(self, cascade_id: str, api_name: str) -> tuple[bool, str]:
        """Request permission from governor to use an API"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            async with self.session.post(
                f"{self.base_url}/permission",
                json={"cascade_id": cascade_id, "api_name": api_name}
            ) as resp:
                data = await resp.json()
                return data.get("allowed", False), data.get("reason", "Unknown")
        except Exception as e:
            # If governor is down, default to allowing (with warning)
            print(f"Warning: Governor unreachable: {e}")
            return True, "Governor offline - proceeding with caution"

    async def record_result(self, cascade_id: str, api_name: str,
                           success: bool, error_message: str = ""):
        """Record cascade execution result"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            async with self.session.post(
                f"{self.base_url}/result",
                json={
                    "cascade_id": cascade_id,
                    "api_name": api_name,
                    "success": success,
                    "error_message": error_message
                }
            ) as resp:
                return await resp.json()
        except Exception as e:
            print(f"Warning: Failed to record result: {e}")

    async def queue_cascade(self, cascade_data: dict) -> Optional[str]:
        """Queue a new cascade for execution"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        try:
            async with self.session.post(
                f"{self.base_url}/cascade",
                json=cascade_data
            ) as resp:
                data = await resp.json()
                return data.get("cascade_id")
        except Exception as e:
            print(f"Error queuing cascade: {e}")
            return None

def governed_cascade(apis_required: list[str]):
    """Decorator to add governor control to cascade functions"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract or generate cascade ID
            cascade_id = kwargs.get("cascade_id", f"cascade_{func.__name__}_{id(args)}")

            async with GovernorClient() as client:
                # Check permissions for all required APIs
                for api in apis_required:
                    allowed, reason = await client.request_permission(cascade_id, api)
                    if not allowed:
                        raise PermissionError(f"Governor blocked {api}: {reason}")

                # Execute the cascade
                try:
                    result = await func(*args, **kwargs)

                    # Record success
                    for api in apis_required:
                        await client.record_result(cascade_id, api, True)

                    return result

                except Exception as e:
                    # Record failure
                    for api in apis_required:
                        await client.record_result(cascade_id, api, False, str(e))
                    raise

        return wrapper
    return decorator

# Example usage in existing scripts
@governed_cascade(apis_required=["github", "airtable"])
async def populate_funding_dashboard():
    """Example of governed cascade function"""
    # Existing implementation would go here
    print("Populating funding dashboard with governor oversight")
    # Simulate work
    await asyncio.sleep(1)
    return {"status": "success", "records": 42}

# Integration helper for existing scripts
class CascadeGovernance:
    """Helper class to integrate governance into existing cascade scripts"""

    def __init__(self):
        self.client = GovernorClient()
        self.cascade_id = None

    async def start_cascade(self, name: str, apis: list[str]) -> str:
        """Start a governed cascade"""
        cascade_data = {
            "name": name,
            "apis": apis,
            "source": "legacy_integration"
        }

        async with self.client as client:
            self.cascade_id = await client.queue_cascade(cascade_data)
            return self.cascade_id

    async def check_api(self, api_name: str) -> bool:
        """Check if API usage is allowed"""
        if not self.cascade_id:
            raise ValueError("No cascade started")

        async with self.client as client:
            allowed, reason = await client.request_permission(self.cascade_id, api_name)
            if not allowed:
                print(f"API {api_name} blocked: {reason}")
            return allowed

    async def report_success(self, api_name: str):
        """Report successful API usage"""
        if not self.cascade_id:
            return

        async with self.client as client:
            await client.record_result(self.cascade_id, api_name, True)

    async def report_failure(self, api_name: str, error: str):
        """Report failed API usage"""
        if not self.cascade_id:
            return

        async with self.client as client:
            await client.record_result(self.cascade_id, api_name, False, error)

# Monkey-patch helper for immediate integration
def patch_existing_function(original_func, apis_required):
    """Patch an existing function to add governance"""
    @wraps(original_func)
    async def governed_func(*args, **kwargs):
        governance = CascadeGovernance()
        cascade_id = await governance.start_cascade(
            name=original_func.__name__,
            apis=apis_required
        )

        # Check all APIs upfront
        for api in apis_required:
            if not await governance.check_api(api):
                raise PermissionError(f"Governor blocked access to {api}")

        try:
            # Run original function
            result = await original_func(*args, **kwargs)

            # Report success
            for api in apis_required:
                await governance.report_success(api)

            return result

        except Exception as e:
            # Report failures
            for api in apis_required:
                await governance.report_failure(api, str(e))
            raise

    return governed_func

# Export for use in other scripts
__all__ = ['GovernorClient', 'governed_cascade', 'CascadeGovernance', 'patch_existing_function']
