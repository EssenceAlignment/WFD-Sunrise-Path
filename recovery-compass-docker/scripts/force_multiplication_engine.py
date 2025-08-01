#!/usr/bin/env python3
"""Force Multiplication Engine for recovery-compass-docker"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from main project if available
try:
    from scripts.force_multiplication_engine import *
    print("✅ Using main force multiplication engine")
except ImportError:
    print("⚠️  Please implement force multiplication engine for this project")
    print("   Reference: WFD-Sunrise-Path/scripts/force_multiplication_engine.py")
