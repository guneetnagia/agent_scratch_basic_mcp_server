#!/bin/bash
set -e

echo "🚀 Starting Idea Hub MCP Server..."

# =========================
# Environment
# =========================
export HF_HOME=./.cache/huggingface
export TRANSFORMERS_CACHE=./.cache/huggingface

mkdir -p "$HF_HOME"

# =========================
# Wait for DB (important)
# =========================
echo "⏳ Waiting for PostgreSQL..."

until nc -z localhost 5432; do
  sleep 1
done

echo "✅ PostgreSQL is ready"

# =========================
# Run server (triggers migrations)
# =========================
echo "🚀 Launching server..."

python src/web_server.py