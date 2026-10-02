#!/usr/bin/env bash
set -e

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Load environment variables if .env exists
if [ -f .env ]; then
  # Export vars without comments
  export $(grep -v '^#' .env | xargs)
fi

DB_USER="${POSTGRES_USER:-n8n}"
DB_NAME="${POSTGRES_DB:-n8n}"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="$PROJECT_ROOT/backups"
BACKUP_FILE="$BACKUP_DIR/n8n_postgres_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "➡️ Creating PostgreSQL backup for database '${DB_NAME}'..."

# Dump database using pg_dump inside container and compress with gzip
docker compose exec -T postgres pg_dump -U "$DB_USER" -d "$DB_NAME" --clean --if-exists | gzip > "$BACKUP_FILE"

echo "✅ Backup successfully created at: $BACKUP_FILE"
echo "📦 Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"
echo ""
echo "💡 To restore this backup in the future, run:"
echo "   gunzip -c $BACKUP_FILE | docker compose exec -T postgres psql -U $DB_USER -d $DB_NAME"
