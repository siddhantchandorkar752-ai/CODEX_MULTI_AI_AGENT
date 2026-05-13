$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . ".\.venv\Scripts\Activate.ps1"
}

$env:PYTHONPATH = (Resolve-Path ".\backend").Path
python -m uvicorn app.api.main:app --host 127.0.0.1 --port 8010
