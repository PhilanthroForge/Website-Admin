#!/bin/bash
# Build script to generate static site from Admin content

BASE_DIR="/Users/bipashahalder/Documents/Philanthroforge_Complete_Clone"
cd "$BASE_DIR"

echo "Building PhilanthroForge Site..."

# Generate index.html from JSON content
if [ -f "run_export.py" ]; then
    python3 run_export.py
    echo "✅ index.html updated from Admin content"
else
    echo "⚠️  run_export.py not found!"
fi

# Run existing component system updates if needed
if [ -f "deploy_all.sh" ]; then
    ./deploy_all.sh
fi

echo "Build Complete!"
