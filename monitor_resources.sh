#!/bin/bash
# Monitor resources used by Plex MCP Server

echo "🔍 Plex MCP Server Resource Usage"
echo "================================="

# Find the process
PID=$(pgrep -f "python main.py")

if [ -n "$PID" ]; then
    echo "Process ID: $PID"
    echo ""
    
    # Get resource usage
    ps -p $PID -o pid,ppid,%cpu,%mem,vsz,rss,comm --no-headers
    echo ""
    
    # Get detailed memory info
    echo "Memory details:"
    cat /proc/$PID/status | grep -E "(VmSize|VmRSS|VmData)"
else
    echo "❌ Process not found"
fi

echo ""
echo "Overall system:"
free -h
echo ""
uptime

