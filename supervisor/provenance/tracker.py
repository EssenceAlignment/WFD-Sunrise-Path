#!/usr/bin/env python3
"""
Provenance Tracker with ED25519 signatures
Maintains audit trail for all automated changes
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import nacl.signing
    import nacl.encoding
    HAS_NACL = True
except (ImportError, Exception) as e:
    HAS_NACL = False
    # Silent fallback - system works without crypto signatures


class ProvenanceTracker:
    """Track and sign all automated changes"""

    RETENTION_DAYS = 30  # Configurable retention period

    def __init__(self, base_path: str = "supervisor"):
        self.base_path = Path(base_path)
        self.keys_dir = self.base_path / ".keys"
        self.logs_dir = self.base_path / "logs" / "snippets"

        # Create directories
        self.keys_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        # Load or generate signing key
        self.signing_key = self._load_or_generate_key() if HAS_NACL else None

    def create_provenance_footer(self, cascade_id: str, agent_id: str,
                                log_snippet: str, governor_run_id: str) -> str:
        """Create signed provenance footer for changes"""
        timestamp = datetime.now().isoformat()

        # Limit log snippet to 20 lines
        snippet_lines = log_snippet.split('\n')[:20]
        truncated_snippet = '\n'.join(snippet_lines)

        footer_content = f"""---
AUTOMATED CHANGE PROVENANCE
Cascade ID: {cascade_id}
Agent: {agent_id}
Governor Run: {governor_run_id}
Timestamp: {timestamp}
Trigger Log:
{truncated_snippet}"""

        # Generate signature if available
        if self.signing_key and HAS_NACL:
            signature = self.generate_signature(footer_content)
            footer_content += f"\nSignature: {signature}"
        else:
            footer_content += "\nSignature: [PyNaCl not installed]"

        footer_content += "\n---"

        # Store snippet for retention
        self._store_snippet(cascade_id, {
            "cascade_id": cascade_id,
            "agent_id": agent_id,
            "governor_run_id": governor_run_id,
            "timestamp": timestamp,
            "log_snippet": truncated_snippet,
            "signature": signature if self.signing_key else None
        })

        return footer_content

    def generate_signature(self, content: str) -> str:
        """Generate ED25519 signature for content"""
        if not self.signing_key or not HAS_NACL:
            return "NO_SIGNATURE"

        message = content.encode('utf-8')
        signed = self.signing_key.sign(message)
        return nacl.encoding.HexEncoder.encode(signed.signature).decode('utf-8')

    def verify_signature(self, content: str, signature: str) -> bool:
        """Verify ED25519 signature"""
        if not self.signing_key or not HAS_NACL:
            return False

        try:
            message = content.encode('utf-8')
            sig_bytes = nacl.encoding.HexEncoder.decode(signature.encode('utf-8'))
            verify_key = self.signing_key.verify_key
            verify_key.verify(message, sig_bytes)
            return True
        except Exception:
            return False

    def _load_or_generate_key(self) -> Optional[Any]:
        """Load existing key or generate new ED25519 key pair"""
        if not HAS_NACL:
            return None

        key_path = self.keys_dir / "provenance_signing.key"

        if key_path.exists():
            try:
                with open(key_path, 'rb') as f:
                    return nacl.signing.SigningKey(f.read())
            except Exception as e:
                print(f"Error loading key: {e}")
                return None
        else:
            # Generate new key
            try:
                key = nacl.signing.SigningKey.generate()
                with open(key_path, 'wb') as f:
                    f.write(key.encode())
                # Also save public key
                pub_key_path = self.keys_dir / "provenance_signing.pub"
                with open(pub_key_path, 'wb') as f:
                    f.write(key.verify_key.encode())
                print(f"Generated new ED25519 key pair at {key_path}")
                return key
            except Exception as e:
                print(f"Error generating key: {e}")
                return None

    def _store_snippet(self, cascade_id: str, data: Dict[str, Any]):
        """Store log snippet for retention"""
        snippet_file = self.logs_dir / f"{cascade_id}.json"
        with open(snippet_file, 'w') as f:
            json.dump(data, f, indent=2)

    def cleanup_old_snippets(self):
        """Remove log snippets older than RETENTION_DAYS"""
        cutoff_date = datetime.now() - timedelta(days=self.RETENTION_DAYS)
        removed_count = 0

        for snippet_file in self.logs_dir.glob("*.json"):
            try:
                with open(snippet_file) as f:
                    data = json.load(f)

                timestamp = datetime.fromisoformat(data["timestamp"])
                if timestamp < cutoff_date:
                    snippet_file.unlink()
                    removed_count += 1
            except Exception as e:
                print(f"Error processing {snippet_file}: {e}")

        print(f"Cleaned up {removed_count} snippets older than "
              f"{self.RETENTION_DAYS} days")
        return removed_count

    def get_snippet(self, cascade_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored snippet by cascade ID"""
        snippet_file = self.logs_dir / f"{cascade_id}.json"
        if snippet_file.exists():
            with open(snippet_file) as f:
                return json.load(f)
        return None

    def list_recent_cascades(self, days: int = 7) -> list:
        """List cascades from the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_cascades = []

        for snippet_file in self.logs_dir.glob("*.json"):
            try:
                with open(snippet_file) as f:
                    data = json.load(f)

                timestamp = datetime.fromisoformat(data["timestamp"])
                if timestamp >= cutoff_date:
                    recent_cascades.append({
                        "cascade_id": data["cascade_id"],
                        "agent_id": data["agent_id"],
                        "timestamp": data["timestamp"]
                    })
            except Exception:
                continue

        return sorted(recent_cascades,
                     key=lambda x: x["timestamp"],
                     reverse=True)


# Example usage
if __name__ == "__main__":
    tracker = ProvenanceTracker()

    # Create a sample provenance footer
    footer = tracker.create_provenance_footer(
        cascade_id="cascade_oauth_fix_123",
        agent_id="infrastructure_agent",
        log_snippet="Error: No redirect uri set!\nAttempting OAuth flow...",
        governor_run_id="gov_run_456"
    )

    print("Generated Provenance Footer:")
    print(footer)

    # Clean up old snippets
    tracker.cleanup_old_snippets()

    # List recent cascades
    recent = tracker.list_recent_cascades(days=1)
    print(f"\nRecent cascades: {len(recent)}")
