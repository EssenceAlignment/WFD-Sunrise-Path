#!/bin/bash

# WFD Dashboard Icon Generation Script
# Generates app icons for iOS and Android from a single source image

set -e

# Colors
PURPLE="#6B46C1"
WHITE="#FFFFFF"

echo "🎨 WFD Dashboard Icon Generator"
echo "================================"

# Check dependencies
check_dependency() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ Error: $1 is required but not installed."
        echo "   Install with: $2"
        exit 1
    fi
}

check_dependency "convert" "brew install imagemagick"
check_dependency "inkscape" "brew install inkscape" || echo "⚠️  Warning: Inkscape not found, using ImageMagick fallback"

# Create resources directory if it doesn't exist
mkdir -p resources/ios
mkdir -p resources/android
mkdir -p resources/store

# Source image path
SOURCE_IMAGE="${1:-resources/icon-source.png}"

if [ ! -f "$SOURCE_IMAGE" ]; then
    echo "📝 Creating placeholder icon..."
    # Create a simple WFD branded icon as placeholder
    convert -size 1024x1024 \
        -background "$PURPLE" \
        -fill "$WHITE" \
        -gravity center \
        -pointsize 400 \
        -font "Helvetica-Bold" \
        label:"WFD" \
        resources/icon-source.png
    SOURCE_IMAGE="resources/icon-source.png"
fi

echo "🔧 Generating iOS icons..."
# iOS Icon Sizes
IOS_SIZES=(
    "20:1x,2x,3x"
    "29:1x,2x,3x"
    "40:1x,2x,3x"
    "60:2x,3x"
    "76:1x,2x"
    "83.5:2x"
    "1024:1x"
)

for size_info in "${IOS_SIZES[@]}"; do
    IFS=':' read -r base_size scales <<< "$size_info"
    IFS=',' read -ra scale_array <<< "$scales"

    for scale in "${scale_array[@]}"; do
        if [ "$scale" == "1x" ]; then
            size=$base_size
        else
            size=$(echo "$base_size * ${scale%x}" | bc)
        fi
        output="resources/ios/icon-${base_size}x${base_size}@${scale}.png"
        echo "  • Creating $output (${size}x${size})"
        convert "$SOURCE_IMAGE" -resize "${size}x${size}" "$output"
    done
done

echo "🤖 Generating Android icons..."
# Android Adaptive Icon Sizes
ANDROID_SIZES=(
    "48:mdpi"
    "72:hdpi"
    "96:xhdpi"
    "144:xxhdpi"
    "192:xxxhdpi"
    "512:store"
)

for size_info in "${ANDROID_SIZES[@]}"; do
    IFS=':' read -r size density <<< "$size_info"

    # Foreground (with padding for adaptive icon)
    fg_output="resources/android/ic_launcher_foreground_${density}.png"
    echo "  • Creating $fg_output (${size}x${size})"
    convert "$SOURCE_IMAGE" \
        -resize "66%" \
        -gravity center \
        -background transparent \
        -extent "${size}x${size}" \
        "$fg_output"

    # Background (solid color)
    bg_output="resources/android/ic_launcher_background_${density}.png"
    convert -size "${size}x${size}" \
        xc:"$PURPLE" \
        "$bg_output"
done

echo "📱 Generating PWA icons..."
# PWA Icon Sizes
PWA_SIZES=(192 512)
for size in "${PWA_SIZES[@]}"; do
    output="resources/icon-${size}.png"
    echo "  • Creating $output (${size}x${size})"
    convert "$SOURCE_IMAGE" -resize "${size}x${size}" "$output"
done

echo "🏪 Generating store assets..."
# Feature Graphic for Google Play
echo "  • Creating feature graphic (1024x500)"
convert -size 1024x500 \
    -background "$PURPLE" \
    -fill "$WHITE" \
    -gravity center \
    -pointsize 150 \
    -font "Helvetica-Bold" \
    label:"WFD Dashboard\nRecovery Compass" \
    resources/store/feature-graphic.png

# App Store Preview
echo "  • Creating App Store preview icon"
convert "$SOURCE_IMAGE" \
    -resize 1024x1024 \
    resources/store/app-store-icon.png

echo ""
echo "✅ Icon generation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Review generated icons in resources/"
echo "2. Update capacitor.config.ts with icon paths"
echo "3. Run 'npm run cap:sync' to apply icons"
echo ""
echo "💡 For custom branding, replace resources/icon-source.png with your logo"
