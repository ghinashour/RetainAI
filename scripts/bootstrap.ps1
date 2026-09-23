$ErrorActionPreference = 'Stop'

Write-Host 'Setting up RetainAI development environment...'

if (-not (Test-Path '.env')) {
    Copy-Item '.env.example' '.env'
    Write-Host 'Created .env from .env.example'
}

python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend\requirements-dev.txt

Set-Location frontend
npm install
Set-Location ..

Write-Host 'Bootstrap complete.'
Write-Host 'Run backend with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000'
Write-Host 'Run frontend with: npm run dev'
Write-Host 'Run docker compose with: docker compose up --build'
