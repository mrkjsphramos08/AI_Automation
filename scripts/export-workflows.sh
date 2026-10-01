#!/usr/bin/env bash
set -e

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "➡️ Exporting all n8n workflows into ./workflows/..."
docker compose exec -T n8n n8n export:workflow --all --output=/workflows/ --backup

echo "✅ Workflows successfully exported to ./workflows/"
echo "💡 You can now review changes with 'git status' and commit your workflows."
