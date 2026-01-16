#!/bin/bash

# FastAPI Application Startup Script
# This script ensures you run uvicorn from the correct directory

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to project root
cd "$SCRIPT_DIR"

# Check if we're in the right directory
if [ ! -d "app" ]; then
    echo "❌ Error: 'app' directory not found!"
    echo "Make sure you're running this script from the project root."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "Please create it with: python3.12 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Check if FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "❌ Error: FastAPI not installed in virtual environment!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Display info
echo "✅ Starting FastAPI application..."
echo "📁 Working directory: $(pwd)"
echo "🐍 Python: $(which python)"
echo "🚀 Running: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "📖 API Documentation will be available at: http://localhost:8000/docs"
echo "❤️  Health check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
