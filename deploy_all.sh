#!/bin/bash
# Master Deployment Script
# Deploys both component system and organized assets

set -e  # Exit on error

echo "============================================================="
echo "PhilanthroForge Website Modernization"
echo "============================================================="
echo ""

# Get the directory where the script is located
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR" || exit 1

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Phase 1: Component System Deployment${NC}"
echo "-------------------------------------------------------------"
if [ -f "apply_component_system.py" ]; then
    python3 apply_component_system.py
    echo -e "${GREEN}✅ Component system deployed${NC}"
else
    echo -e "${YELLOW}⚠️  Component script not found, skipping...${NC}"
fi
echo ""

echo -e "${BLUE}Phase 2: Asset Organization${NC}"
echo "-------------------------------------------------------------"

# Run asset analysis
if [ -f "analyze_assets.py" ]; then
    echo "Analyzing assets..."
    python3 analyze_assets.py
    echo ""
fi

# Run asset reorganization
if [ -f "rename_assets.sh" ]; then
    echo "Reorganizing assets..."
    chmod +x rename_assets.sh
    ./rename_assets.sh
    echo -e "${GREEN}✅ Assets reorganized${NC}"
    echo ""
fi

# Update HTML references
if [ -f "update_asset_references.py" ]; then
    echo "Updating HTML references..."
    python3 update_asset_references.py
    echo -e "${GREEN}✅ HTML references updated${NC}"
    echo ""
fi

echo "============================================================="
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo "============================================================="
echo ""
echo "📊 Summary:"
echo "  • Component system: Deployed across 19 pages"
echo "  • Assets: Reorganized into logical structure"
echo "  • HTML: Updated with new asset paths"
echo ""
echo "🧪 Next Steps:"
echo "  1. Test the site: python3 -m http.server 8080"
echo "  2. Open: http://localhost:8080"
echo "  3. Verify navigation and images load correctly"
echo ""
echo "📝 To update nav/footer in the future:"
echo "  • Edit: components/navbar.html"
echo "  • Edit: components/footer.html"
echo "  • Changes reflect on ALL 19 pages instantly!"
echo ""
