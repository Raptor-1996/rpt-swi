#!/bin/bash
# Build Package Script

set -e

echo "Building RPT SWI Package..."
echo "============================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Create distribution packages
echo -e "${BLUE}Creating source distribution...${NC}"
python3 setup.py sdist

echo -e "${BLUE}Creating wheel distribution...${NC}"
python3 setup.py bdist_wheel

echo -e "${BLUE}Creating standalone executable...${NC}"
# Note: pyinstaller would need to be installed
# pyinstaller --onefile --name rpt-swi src/main.py

# Create archive for manual installation
echo -e "${BLUE}Creating archive...${NC}"
VERSION=$(python3 -c "import setup; print(setup.version)" 2>/dev/null || echo "2.0.0")
ARCHIVE_NAME="rpt-swi-${VERSION}.tar.gz"

tar -czf ${ARCHIVE_NAME} \
    --exclude="*.pyc" \
    --exclude="__pycache__" \
    --exclude=".git" \
    --exclude=".vscode" \
    --exclude=".idea" \
    src/ \
    docs/ \
    config/ \
    tests/ \
    requirements.txt \
    README.md \
    LICENSE \
    INSTALL.md \
    QUICKSTART.md \
    setup.py \
    install.sh \
    uninstall.sh \
    quickstart.sh \
    test_installation.sh \
    Dockerfile \
    docker-compose.yml \
    .gitignore

echo -e "${GREEN}Build complete!${NC}"
echo ""
echo "Created files:"
echo "  dist/rpt_swi-${VERSION}.tar.gz  - Source distribution"
echo "  dist/rpt_swi-${VERSION}-py3-none-any.whl  - Wheel package"
echo "  ${ARCHIVE_NAME}  - Manual installation archive"
echo ""
echo "To upload to PyPI:"
echo "  twine upload dist/*"
echo ""
echo "To install locally:"
echo "  pip install dist/rpt_swi-${VERSION}-py3-none-any.whl"
