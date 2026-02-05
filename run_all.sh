#!/bin/bash
# Complete workflow: scrape, transform, and serve

set -e

echo "=========================================="
echo "Danish Vet Med Flash Cards - Full Workflow"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then run: source venv/bin/activate"
    echo "Then run: pip install -r scraper/requirements.txt"
    exit 1
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Virtual environment not activated!"
    echo "Please run: source venv/bin/activate"
    exit 1
fi

# Ask user which mode to run
echo "Select mode:"
echo "1) Test mode (first 3 medications)"
echo "2) Full scrape (all 75 medications)"
read -p "Enter choice (1 or 2): " choice

echo ""
echo "Step 1/3: Running scraper..."
echo "=========================================="

if [ "$choice" == "1" ]; then
    cd scraper
    python3 scraper.py --test
    cd ..
elif [ "$choice" == "2" ]; then
    cd scraper
    python3 scraper.py
    cd ..
else
    echo "❌ Invalid choice"
    exit 1
fi

echo ""
echo "Step 2/3: Transforming data for frontend..."
echo "=========================================="
python3 transform_data.py

echo ""
echo "Step 3/3: Starting local server..."
echo "=========================================="
echo ""
echo "✅ Setup complete! Starting server..."
echo ""
python3 server.py
