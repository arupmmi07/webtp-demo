#!/bin/bash
# Render.com startup script
# Initializes data files and starts the API server

set -e  # Exit on error

echo "🚀 Starting Healthcare Operations Assistant on Render..."
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/backups logs static

# Initialize data files if they don't exist
echo "📋 Checking data files..."

if [ ! -f data/appointments.json ]; then
    echo "  ➡️  Copying appointments.json from backup..."
    cp data/backups/appointments.json.template data/appointments.json 2>/dev/null || echo "[]" > data/appointments.json
fi

if [ ! -f data/patients.json ]; then
    echo "  ➡️  Copying patients.json from backup..."
    cp data/backups/patients.json.template data/patients.json 2>/dev/null || echo "[]" > data/patients.json
fi

if [ ! -f data/providers.json ]; then
    echo "  ➡️  Copying providers.json from backup..."
    cp data/backups/providers.json.template data/providers.json 2>/dev/null || echo "[]" > data/providers.json
fi

if [ ! -f data/waitlist.json ]; then
    echo "  ➡️  Initializing waitlist.json..."
    cp data/backups/waitlist.json.template data/waitlist.json 2>/dev/null || echo "[]" > data/waitlist.json
fi

if [ ! -f data/freed_slots.json ]; then
    echo "  ➡️  Initializing freed_slots.json..."
    cp data/backups/freed_slots.json.template data/freed_slots.json 2>/dev/null || echo "[]" > data/freed_slots.json
fi

if [ ! -f data/emails.json ]; then
    echo "  ➡️  Initializing emails.json..."
    echo "[]" > data/emails.json
fi

echo ""
echo "✅ Data files initialized"
echo ""
echo "🌐 Starting API server on port ${PORT:-8000}..."
echo ""

# Start the API server
exec uvicorn api.server:app --host 0.0.0.0 --port ${PORT:-8000}

