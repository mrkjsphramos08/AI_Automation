#!/usr/bin/env bash
set -e

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "➡️ Importing workflows from ./workflows/ into n8n..."
docker compose exec -T n8n n8n import:workflow --separate --input=/workflows/

echo "✅ Workflows successfully imported into n8n."
