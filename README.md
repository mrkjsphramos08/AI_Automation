# AI Automation Workspace

A containerized automation environment built on [n8n](https://n8n.io/) designed for building, testing, and managing AI agent workflows, integrations, and automated pipelines.

---

## 📁 Repository Structure

```text
ai-automation/
├── .env.example              # Environment variables template
├── .gitignore                # Protects secrets, databases, and runtime files
├── docker-compose.yml        # Docker service definitions (n8n, postgres, ai-service)
├── docs/
│   └── learning-log.md       # Architectural notes & concepts learned
├── services/
│   └── ai-service/           # Python FastAPI AI microservice
│       ├── Dockerfile
│       ├── requirements.txt
│       └── main.py
├── workflows/                # Exported workflow JSON files (version-controlled)
├── scripts/
│   ├── export-workflows.sh   # Exports workflows from n8n to ./workflows/
│   ├── import-workflows.sh   # Imports workflows from ./workflows/ into n8n
│   └── backup-db.sh          # Compressed PostgreSQL database dump (pg_dump)
├── shared-data/              # Local storage for documents, CSVs, or media
└── README.md                 # Project documentation & setup instructions
```

---

## 🚀 Quick Start

### 1. Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose installed.

### 2. Configure Environment
Copy the example environment file:
```bash
cp .env.example .env
```
Generate an encryption key or leave the existing one configured in `.env`.

### 3. Start the Stack
```bash
docker compose up -d
```

### 4. Access n8n
Open your browser and navigate to:
```
http://localhost:5678
```
Follow the on-screen instructions to create your initial owner account.

### 5. Access Python AI Microservice (FastAPI)
The Python service runs alongside n8n with auto-reloading:
- **Interactive Swagger UI**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`
- **Internal URL (used inside n8n)**: `http://ai-service:8000`

---

## 🔄 Workflow Version Control (Git)

By default, n8n saves workflows inside its internal database (`database.sqlite`), which is git-ignored for security and performance. To version-control your workflows on GitHub:

### Exporting Workflows
Whenever you create or update workflows in the n8n interface, run:
```bash
chmod +x scripts/*.sh    # Only needed once
./scripts/export-workflows.sh
```
This exports your workflows as JSON files into the `workflows/` directory.

### Restoring Workflows (e.g., on a new machine)
```bash
./scripts/import-workflows.sh
```

> **Security Note:** n8n's export command strips saved credentials and API keys from exported workflow files automatically. However, always ensure you never hardcode sensitive keys directly into raw strings or custom Code/HTTP Request nodes.

---

## 🗄️ Database Backups & Restore (PostgreSQL)

n8n runs on a containerized PostgreSQL database (`postgres:16-alpine`) backed by a Docker named volume (`postgres-data`).

### Creating a Database Backup
To create a compressed snapshot of the entire database (including users, credentials, workflows, and execution logs):
```bash
./scripts/backup-db.sh
```
This saves a timestamped, gzip-compressed SQL dump in `backups/` (e.g., `backups/n8n_postgres_YYYYMMDD_HHMMSS.sql.gz`).

### Restoring a Database Backup
```bash
gunzip -c backups/n8n_postgres_<TIMESTAMP>.sql.gz | docker compose exec -T postgres psql -U n8n -d n8n
```

---

## 📤 How to Publish to GitHub

Follow these steps to safely publish this repository to your GitHub account:

### 1. Verify Ignored Files (Security Check)
Ensure secrets (`.env`) and local data (`.n8n-data/`) are excluded:
```bash
git status
```
Confirm that neither `.env` nor `.n8n-data/` appears in the list of untracked files.

### 2. Stage and Commit Your Project Files
```bash
git add .
git commit -m "feat: initial setup for ai automation workspace"
```

### 3. Create a Remote Repository on GitHub
1. Go to [GitHub.com/new](https://github.com/new).
2. Name your repository (e.g. `ai-automation`).
3. Set the repository visibility (**Public** or **Private**).
4. **Leave "Initialize this repository with a README" unchecked** (you already have one).
5. Click **Create repository**.

### 4. Link Remote and Push
Copy your repository URL from GitHub and run:
```bash
# Rename default branch to main
git branch -M main

# Add your GitHub repository as origin (replace with your repository URL)
git remote add origin https://github.com/<YOUR_USERNAME>/ai-automation.git

# Push your code
git push -u origin main
```

---

## 🛠️ Configuration & Customization

### Execution History Pruning
Execution logs are configured to automatically prune after 7 days (`EXECUTIONS_DATA_MAX_AGE=168`) to keep disk space lean and performance fast.

### File Access & Shared Data
- **Permissions**: The `shared-data/` directory is pre-created in this repository. n8n runs as the `node` user (UID 1000), which matches standard Linux file ownership.
- **Restricted Access**: If your n8n version enforces file access restrictions on the Read/Write Files from Disk node, you can set `N8N_RESTRICT_FILE_ACCESS_TO=/data/shared` in `docker-compose.yml`.
