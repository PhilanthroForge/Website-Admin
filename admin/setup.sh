#!/bin/bash
# Admin Panel Setup Script

echo "============================================================="
echo "PhilanthroForge Admin Panel Setup"
echo "============================================================="
echo ""

cd /Users/bipashahalder/Documents/Philanthroforge_Complete_Clone/admin

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "============================================================="
echo "✅ Setup Complete!"
echo "============================================================="
echo ""
echo "To run the admin panel:"
echo ""
echo "  cd admin"
echo "  source venv/bin/activate"
echo "  python3 app.py"
echo ""
echo "Then visit: http://localhost:5000/admin"
echo ""
echo "Default credentials:"
echo "  Email: admin@philanthroforge.com"
echo "  Password: ChangeMe123!"
echo ""
echo "⚠️  CHANGE THE PASSWORD AFTER FIRST LOGIN!"
echo "============================================================="
