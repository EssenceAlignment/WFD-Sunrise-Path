"""
Provenance tracking system for automated changes
Ensures audit trail and integrity of all cascade operations
"""

from .tracker import ProvenanceTracker

__all__ = ['ProvenanceTracker']
