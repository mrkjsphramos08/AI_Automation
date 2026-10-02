# Learning Log & Architectural Notes

## Session: SQLite to PostgreSQL Migration & Python Integration

### 1. What We Built & Migrated
- **PostgreSQL Database Service**: Replaced local SQLite (`database.sqlite`) with a containerized PostgreSQL 16 Alpine service.
- **Python AI Microservice**: Built a FastAPI service running in Docker Compose with hot-reloading for custom AI and data manipulation.
- **Workflow Version Control & Backups**:
  - Exported n8n workflows into version-controlled JSON files in `workflows/`.
  - Added an automated compressed database backup script (`scripts/backup-db.sh`) using `pg_dump` and `gzip`.

---

### 2. Core Concepts Learned

#### A. Docker Networking & DNS
- Containers in the same Docker network cannot communicate via `localhost` because `localhost` refers to the container itself.
- Docker provides internal DNS resolution:
  - n8n reaches Postgres using host `postgres` on port `5432`.
  - n8n reaches the Python API using host `ai-service` on port `8000`.
- No host port publication (`ports: - "5432:5432"`) is needed for Postgres unless external host GUI clients (e.g. pgAdmin/DBeaver) require access.

#### B. Named Volumes vs Bind Mounts
- **Bind mounts** (`./.n8n-data:/home/node/.n8n`): Map directly to host paths. Great for user-facing scripts and workflows, but prone to permission and I/O friction on WSL2/Windows.
- **Named volumes** (`postgres-data:/var/lib/postgresql/data`): Managed directly by Docker inside the native Linux disk. Ideal for databases requiring strict POSIX permissions and high-throughput write performance (`fsync`).

#### C. Startup Dependencies & Healthchecks
- Plain `depends_on: [postgres]` only waits for the process to be spawned, which leads to `ECONNREFUSED` crashes while Postgres runs `initdb`.
- Using `depends_on: postgres: condition: service_healthy` coupled with `pg_isready` ensures n8n only boots once PostgreSQL is genuinely accepting SQL connections.

#### D. n8n Security & Encryption Key
- n8n uses AES-256 to encrypt all stored credentials (API tokens, OAuth tokens, passwords).
- The encryption key must be explicitly pinned via `N8N_ENCRYPTION_KEY` in `.env` across migrations; otherwise, encrypted credentials cannot be decrypted if keys diverge.
- Workflows exported with `export:workflow` strip credential secrets for Git safety; credentials must be verified or re-authenticated after database migrations.

---

### 3. Key Commands Reference
```bash
# Export all workflows from n8n to workflows/
./scripts/export-workflows.sh

# Import workflows from workflows/ to n8n
./scripts/import-workflows.sh

# Create a compressed PostgreSQL backup
./scripts/backup-db.sh

# Restore a PostgreSQL backup
gunzip -c backups/n8n_postgres_<TIMESTAMP>.sql.gz | docker compose exec -T postgres psql -U n8n -d n8n

# Query Postgres tables inside the container
docker compose exec postgres psql -U n8n -d n8n -c '\dt'
```
