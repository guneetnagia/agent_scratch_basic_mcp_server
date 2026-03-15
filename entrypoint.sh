#!/bin/bash

set -e

echo "🚀 Starting Basic agent scratch MCP Server..."

# HuggingFace cache
export HF_HOME=./.cache/huggingface
export TRANSFORMERS_CACHE=./.cache/huggingface

# Allow downloading models
export HF_HUB_OFFLINE=0
export TRANSFORMERS_OFFLINE=0

# Create cache directory
if [ ! -d "$HF_HOME" ]; then
    echo "📁 Creating HuggingFace cache directory: $HF_HOME"
    mkdir -p "$HF_HOME"
fi

echo "🔍 Checking MCP server import..."

python -c "from src.main import main; print('✅ MCP server imported successfully')" || {
    echo "❌ Failed to import MCP server"
    exit 1
}

echo "✅ Environment setup complete. Starting MCP server..."

python src/web_server.py