#!/bin/bash
# Render.com startup script for Web UI
# Starts the FastAPI server with HTML pages (replaces Streamlit)

set -e  # Exit on error

echo "🎨 Starting Web UI on Render..."
echo ""
echo "🌐 API Connection: ${API_BASE_URL:-http://localhost:8000}"
echo "🔧 Port: ${PORT:-8501}"
echo ""

# Create necessary directories
mkdir -p logs static

echo "✅ Starting FastAPI Web Server..."
echo "   📅 Schedule: /schedule.html"
echo "   📧 Emails: /emails.html"
echo "   🔄 Reset: /reset.html"
echo ""

# Start the web server (backwards compatible with Streamlit command)
exec python3 demo/chat_ui.py

