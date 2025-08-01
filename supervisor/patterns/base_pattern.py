#!/usr/bin/env python3
"""
Base Pattern Class for Multi-Domain Pattern Registry
Extends ErrorPattern to support funding, donor, and ops domains
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class DomainPattern:
    """Extended pattern class supporting multiple domains with force multiplication"""
    name: str
    pattern: str
    domain: str  # auth, funding, donor, ops
    severity: str
    agent: str
    resolution: str
    force_multiplier: int = 10
    context_hints: List[str] = field(default_factory=list)
    allowed_sources: List[str] = field(default_factory=list)
    compliance_tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.regex = re.compile(self.pattern)
        self.created_at = datetime.now().isoformat()
        self.version = "1.0.0"

    def match(self, text: str, source: str = None) -> Optional[Dict[str, Any]]:
        """Enhanced matching with source validation"""
        # Check if source is allowed for this pattern
        if source and self.allowed_sources and source not in self.allowed_sources:
            return None

        match = self.regex.search(text)
        if match:
            return {
                "matched": True,
                "text": match.group(0),
                "position": match.span(),
                "domain": self.domain,
                "force_multiplier": self.force_multiplier,
                "compliance_tags": self.compliance_tags
            }
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Export pattern to dictionary for registry"""
        return {
            "name": self.name,
            "pattern": self.pattern,
            "domain": self.domain,
            "severity": self.severity,
            "agent": self.agent,
            "resolution": self.resolution,
            "force_multiplier": self.force_multiplier,
            "context_hints": self.context_hints,
            "allowed_sources": self.allowed_sources,
            "compliance_tags": self.compliance_tags,
            "version": self.version,
            "created_at": self.created_at
        }


class PatternRegistry:
    """Unified registry for all domain patterns"""

    def __init__(self):
        self.patterns = {}
        self.shadow_mode = True  # C-1: Default to shadow mode
        self.coverage_metrics = {
            "auth": 0,
            "funding": 0,
            "donor": 0,
            "ops": 0
        }

    def register_pattern(self, pattern: DomainPattern):
        """Register a pattern with the registry"""
        if pattern.domain not in self.patterns:
            self.patterns[pattern.domain] = {}
        self.patterns[pattern.domain][pattern.name] = pattern
        self._update_coverage()

    def detect_all(self, text: str, source: str = None) -> List[Dict[str, Any]]:
        """Detect all matching patterns across domains"""
        detections = []
        for domain, domain_patterns in self.patterns.items():
            for pattern_name, pattern in domain_patterns.items():
                match = pattern.match(text, source)
                if match:
                    match["pattern_name"] = pattern_name
                    match["shadow_mode"] = self.shadow_mode
                    detections.append(match)
        return detections

    def _update_coverage(self):
        """Update coverage metrics for each domain"""
        for domain in self.coverage_metrics:
            if domain in self.patterns:
                self.coverage_metrics[domain] = len(self.patterns[domain])

    def get_coverage_report(self) -> Dict[str, Any]:
        """Get pattern coverage statistics"""
        total_patterns = sum(self.coverage_metrics.values())
        return {
            "total_patterns": total_patterns,
            "by_domain": self.coverage_metrics,
            "shadow_mode": self.shadow_mode,
            "timestamp": datetime.now().isoformat()
        }
