#!/bin/bash
BACKUP_DIR="$(dirname "$0")"
DATE=$(date +%Y%m%d_%H%M%S)

# Dump postgres
docker compose exec -T postgres pg_dump -U n8n n8n > "$BACKUP_DIR/n8n_backup_$DATE.sql"

# Keep last 7 days
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete

echo "Backup complete: n8n_backup_$DATE.sql"
