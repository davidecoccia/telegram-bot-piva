#!/bin/bash

# Setup script for Expense Tracker Bot

echo "🚀 Setting up Expense Tracker Bot..."

# Check if poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed. Please install it first:"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.dist .env
    echo "⚠️  Please edit .env file and add your credentials:"
    echo "   - BOT_TOKEN (from @BotFather)"
    echo "   - AWS_BEARER_TOKEN_BEDROCK (from AWS Console → Bedrock → API Keys)"
    echo "   - AWS_REGION (default: us-east-1)"
fi

# Create necessary directories
echo "📁 Creating storage directories..."
mkdir -p receipts_data
mkdir -p temp_images

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: poetry run python -m src.bot"
