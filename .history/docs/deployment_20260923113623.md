# Deployment and development

## Development environment

Use PowerShell commands on Windows.

```powershell
cd c:\Users\HP\Documents\PROJECTS\RetainAI
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements-dev.txt
```

## Run backend locally

```powershell
cd c:\Users\HP\Documents\PROJECTS\RetainAI\backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Run frontend locally

```powershell
cd c:\Users\HP\Documents\PROJECTS\RetainAI\frontend
npm install
npm run dev
```

## Run with Docker Compose

```powershell
cd c:\Users\HP\Documents\PROJECTS\RetainAI\docker
docker compose up --build
```

## Alembic commands

```powershell
cd c:\Users\HP\Documents\PROJECTS\RetainAI\backend
alembic revision -m "initial_schema"
alembic upgrade head
alembic current
alembic history
```

## Notes

- PostgreSQL data is persisted through a Docker volume.
- Local environment should continue to use .env files and not commit real secrets.
- Docker Compose is for development only in Phase 1.
