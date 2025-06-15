#!/bin/bash
# Simple setup script for Plex MCP Server

echo "🎬 Setting up Plex MCP Server..."

# Copy environment template
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
else
    echo "⚠️  .env file already exists, skipping copy"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🎯 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Plex server details"
echo "2. Run: python main.py"
echo ""
echo "Get your Plex token: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/"

