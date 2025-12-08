#!/bin/bash
# Render.com startup script for Streamlit UI
# Starts the Streamlit chat interface

set -e  # Exit on error

echo "🎨 Starting Streamlit UI on Render..."
echo ""
echo "🌐 API Connection: ${API_BASE_URL:-http://localhost:8000}"
echo "🔧 Port: ${PORT:-8501}"
echo ""

# Create necessary directories
mkdir -p logs

echo "✅ Starting Streamlit..."
echo ""

# Start Streamlit with proper configuration for Render
exec streamlit run demo/chat_ui.py \
    --server.address 0.0.0.0 \
    --server.port ${PORT:-8501} \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --browser.gatherUsageStats false

