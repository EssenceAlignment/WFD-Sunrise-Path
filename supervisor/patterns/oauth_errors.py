#!/usr/bin/env python3
"""
OAuth Error Pattern Detection and Resolution
Identifies OAuth authentication errors and triggers resolution cascades
"""

import re
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class ErrorPattern:
    """Definition of an error pattern"""
    name: str
    pattern: str
    severity: str
    agent: str
    resolution: str
    context_hints: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.regex = re.compile(self.pattern)

    def match(self, text: str) -> Optional[re.Match]:
        """Check if pattern matches text"""
        return self.regex.search(text)


class OAuthErrorPatterns:
    """OAuth error pattern detection and management"""

    def __init__(self):
        self.patterns = self._load_patterns()
        self.detection_history = defaultdict(list)

    def _load_patterns(self) -> Dict[str, ErrorPattern]:
        """Load OAuth error patterns"""
        patterns = {
            "oauth_redirect": ErrorPattern(
                name="oauth_redirect",
                pattern=r"No redirect uri set!",
                severity="high",
                agent="infrastructure",
                resolution="oauth_to_token_migration",
                context_hints=["cloudflare", "mcp", "authentication"]
            ),
            "oauth_custom_scheme": ErrorPattern(
                name="oauth_custom_scheme",
                pattern=r"Custom scheme URI not allowed",
                severity="high",
                agent="security",
                resolution="update_oauth_config",
                context_hints=["google", "oauth", "redirect"]
            ),
            "oauth_token_expired": ErrorPattern(
                name="oauth_token_expired",
                pattern=r"(token expired|invalid_token|token_expired)",
                severity="medium",
                agent="security",
                resolution="refresh_token",
                context_hints=["expiration", "refresh", "credentials"]
            ),
            "oauth_scope_invalid": ErrorPattern(
                name="oauth_scope_invalid",
                pattern=r"(invalid_scope|insufficient_scope)",
                severity="high",
                agent="security",
                resolution="update_scope_permissions",
                context_hints=["permissions", "scopes", "authorization"]
            ),
            "api_key_missing": ErrorPattern(
                name="api_key_missing",
                pattern=r"(API key not found|Missing API key|No API key provided)",
                severity="high",
                agent="infrastructure",
                resolution="configure_api_key",
                context_hints=["environment", "configuration", "credentials"]
            ),
            "auth_config_mismatch": ErrorPattern(
                name="auth_config_mismatch",
                pattern=r"Authentication method mismatch",
                severity="medium",
                agent="devops",
                resolution="align_auth_methods",
                context_hints=["config", "mcp", "authentication"]
            )
        }
        return patterns

    def detect_patterns(self, log_content: str,
                       source: str = "unknown") -> List[Dict[str, any]]:
        """Detect error patterns in log content"""
        detections = []

        for pattern_name, pattern in self.patterns.items():
            match = pattern.match(log_content)
            if match:
                detection = {
                    "pattern_name": pattern_name,
                    "severity": pattern.severity,
                    "agent": pattern.agent,
                    "resolution": pattern.resolution,
                    "match_text": match.group(0),
                    "source": source,
                    "timestamp": datetime.now().isoformat(),
                    "context_hints": pattern.context_hints
                }
                detections.append(detection)
                self.detection_history[pattern_name].append(detection)

        return detections

    def get_resolution_cascade(self, pattern_name: str) -> Dict[str, any]:
        """Get resolution cascade for a specific pattern"""
        if pattern_name not in self.patterns:
            return None

        pattern = self.patterns[pattern_name]

        cascades = {
            "oauth_to_token_migration": {
                "name": "OAuth to API Token Migration",
                "steps": [
                    "identify_auth_method",
                    "locate_api_token_config",
                    "update_mcp_config",
                    "validate_configuration",
                    "update_documentation",
                    "notify_stakeholders"
                ],
                "apis_required": ["filesystem", "github"],
                "estimated_time": 300,  # seconds
                "force_multiplier": 10
            },
            "update_oauth_config": {
                "name": "Update OAuth Configuration",
                "steps": [
                    "identify_oauth_provider",
                    "check_redirect_requirements",
                    "update_oauth_settings",
                    "test_auth_flow",
                    "document_changes",
                    "propagate_to_projects"
                ],
                "apis_required": ["cloudflare", "github"],
                "estimated_time": 600,
                "force_multiplier": 8
            },
            "refresh_token": {
                "name": "Refresh OAuth Token",
                "steps": [
                    "check_token_status",
                    "request_new_token",
                    "update_credentials",
                    "test_authentication",
                    "log_renewal"
                ],
                "apis_required": ["oauth_provider"],
                "estimated_time": 120,
                "force_multiplier": 5
            },
            "update_scope_permissions": {
                "name": "Update OAuth Scopes",
                "steps": [
                    "analyze_required_scopes",
                    "update_oauth_app",
                    "request_user_consent",
                    "validate_permissions",
                    "document_scope_changes"
                ],
                "apis_required": ["oauth_provider", "github"],
                "estimated_time": 450,
                "force_multiplier": 7
            },
            "configure_api_key": {
                "name": "Configure API Key",
                "steps": [
                    "generate_api_key",
                    "store_securely",
                    "update_env_config",
                    "validate_access",
                    "update_documentation"
                ],
                "apis_required": ["filesystem", "github"],
                "estimated_time": 180,
                "force_multiplier": 6
            },
            "align_auth_methods": {
                "name": "Align Authentication Methods",
                "steps": [
                    "audit_current_methods",
                    "identify_conflicts",
                    "standardize_approach",
                    "update_all_configs",
                    "test_integrations",
                    "document_standard"
                ],
                "apis_required": ["filesystem", "github", "airtable"],
                "estimated_time": 900,
                "force_multiplier": 12
            }
        }

        return cascades.get(pattern.resolution)

    def analyze_pattern_frequency(self, days: int = 7) -> Dict[str, int]:
        """Analyze pattern frequency over time"""
        frequency = {}
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)

        for pattern_name, detections in self.detection_history.items():
            recent_count = sum(
                1 for d in detections
                if datetime.fromisoformat(d["timestamp"]).timestamp() > cutoff
            )
            if recent_count > 0:
                frequency[pattern_name] = recent_count

        return frequency

    def suggest_new_patterns(self, unmatched_logs: List[str]) -> List[Dict[str, any]]:
        """Suggest new patterns based on unmatched logs"""
        # This could use ML/clustering in production
        # For now, simple keyword extraction
        suggestions = []

        keyword_counts = defaultdict(int)
        for log in unmatched_logs:
            # Extract potential error keywords
            error_words = re.findall(r'\b(error|failed|invalid|missing|denied)\b',
                                    log.lower())
            for word in error_words:
                keyword_counts[word] += 1

        # Suggest patterns for frequent keywords
        for keyword, count in keyword_counts.items():
            if count >= 3:  # Threshold for suggestion
                suggestions.append({
                    "keyword": keyword,
                    "frequency": count,
                    "suggested_pattern": f".*{keyword}.*",
                    "confidence": min(count / len(unmatched_logs), 0.8)
                })

        return sorted(suggestions, key=lambda x: x["frequency"], reverse=True)

    def export_patterns(self, output_file: str):
        """Export patterns to JSON for sharing"""
        export_data = {
            "patterns": {
                name: {
                    "pattern": p.pattern,
                    "severity": p.severity,
                    "agent": p.agent,
                    "resolution": p.resolution,
                    "context_hints": p.context_hints
                }
                for name, p in self.patterns.items()
            },
            "frequency": self.analyze_pattern_frequency(),
            "exported_at": datetime.now().isoformat()
        }

        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)

    def import_patterns(self, input_file: str):
        """Import patterns from JSON"""
        with open(input_file) as f:
            data = json.load(f)

        for name, pattern_data in data.get("patterns", {}).items():
            if name not in self.patterns:
                self.patterns[name] = ErrorPattern(
                    name=name,
                    **pattern_data
                )


# Example usage
if __name__ == "__main__":
    detector = OAuthErrorPatterns()

    # Test detection
    test_log = """
    2025-01-31 10:15:23 ERROR: No redirect uri set!
    Failed to authenticate with Cloudflare MCP.
    """

    detections = detector.detect_patterns(test_log, source="cloudflare-mcp")

    for detection in detections:
        print(f"Detected: {detection['pattern_name']}")
        print(f"Severity: {detection['severity']}")
        print(f"Resolution: {detection['resolution']}")

        cascade = detector.get_resolution_cascade(detection['pattern_name'])
        if cascade:
            print(f"Cascade: {cascade['name']}")
            print(f"Steps: {', '.join(cascade['steps'])}")
            print(f"Estimated time: {cascade['estimated_time']}s")
