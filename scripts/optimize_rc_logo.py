#!/usr/bin/env python3
"""Optimize Recovery Compass logo for web embedding"""

import base64
import os

# Read the Recovery Compass logo
logo_path = "Recovery Compass Logos/Recovery Compass Official Logo July 31 2025.png"

if os.path.exists(logo_path):
    with open(logo_path, 'rb') as f:
        logo_data = f.read()

    # Convert to base64
    logo_b64 = base64.b64encode(logo_data).decode('utf-8')

    print(f"Logo size: {len(logo_data):,} bytes")
    print(f"Base64 length: {len(logo_b64):,} characters")

    # For large images, we'll reference the file directly instead
    print("\nDue to the large size, we'll reference the logo file directly in the HTML.")

else:
    print(f"Logo not found at: {logo_path}")
