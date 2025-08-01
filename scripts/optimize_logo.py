#!/usr/bin/env python3
"""Optimize Recovery Compass logo for web use"""

from PIL import Image
import base64
import io

# Open and resize the logo
img = Image.open('Recovery Compass Logos/Recovery Compass Official Logo July 31 2025.png')

# Convert to RGB if necessary (removes alpha channel if present)
if img.mode in ('RGBA', 'LA'):
    background = Image.new('RGB', img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
    img = background

# Resize to reasonable dimensions for header (max width 200px)
aspect_ratio = img.width / img.height
new_width = 200
new_height = int(new_width / aspect_ratio)
img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

# Save to bytes
img_buffer = io.BytesIO()
img_resized.save(img_buffer, format='JPEG', quality=85, optimize=True)
img_bytes = img_buffer.getvalue()

# Convert to base64
b64_logo = base64.b64encode(img_bytes).decode('utf-8')

print(f"Original size: {img.width}x{img.height}")
print(f"Optimized size: {new_width}x{new_height}")
print(f"Base64 length: {len(b64_logo)} characters")
print(f"\nBase64 preview (first 100 chars): {b64_logo[:100]}...")

# Save the base64 to a file for use
with open('scripts/rc_logo_base64.txt', 'w') as f:
    f.write(b64_logo)

print("\nBase64 logo saved to scripts/rc_logo_base64.txt")
