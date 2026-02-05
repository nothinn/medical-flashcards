#!/bin/bash
# Quick start script for the flash cards project

set -e

echo "======================================"
echo "Danish Vet Med Flash Cards - Quick Start"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -q -r scraper/requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run scraper (test): cd scraper && python3 scraper.py --test"
echo "2. Run scraper (full):  cd scraper && python3 scraper.py"
echo "3. Transform data:      python3 transform_data.py"
echo "4. Test locally:        python3 server.py"
echo ""
echo "See README.md for full documentation."
