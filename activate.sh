#!/bin/bash
# Quick activation script for the virtual environment

echo "🚀 Activating virtual environment..."
source .venv/bin/activate

echo "✅ Virtual environment activated!"
echo ""
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo ""
echo "📦 Key packages installed:"
pip list | grep -E "(aiogram|strands|boto3|aiofiles|pillow)" | sed 's/^/  /'
echo ""
echo "💡 Quick commands:"
echo "  - Run bot: python -m src.bot"
echo "  - Test scanner: python test_receipt_scanner.py"
echo "  - Deactivate: deactivate"
echo ""
