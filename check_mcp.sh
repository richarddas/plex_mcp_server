#!/bin/bash
# Simple monitoring script for Plex MCP Server

echo "🎬 Plex MCP Server Status Check"
echo "================================"

# Check if service is running
if systemctl is-active --quiet plex-mcp; then
    echo "✅ Service: Running"
else
    echo "❌ Service: Not running"
    exit 1
fi

# Check HTTP endpoint
if curl -s http://localhost:8000/health >/dev/null; then
    echo "✅ HTTP: Responding"
else
    echo "❌ HTTP: Not responding"
    exit 1
fi

# Get detailed status
echo ""
echo "📊 Detailed Status:"
curl -s http://localhost:8000/status | python3 -m json.tool

echo ""
echo "📝 Recent logs:"
sudo journalctl -u plex-mcp -n 5 --no-pager

