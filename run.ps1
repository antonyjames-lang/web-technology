# Yojana Mitra PowerShell Launcher
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Launching Yojana Mitra - Civic Eligibility Identifier" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptDir\backend"

$venvPython = "$scriptDir\venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    Write-Host "[1/3] Using virtualenv Python: $venvPython" -ForegroundColor Green
    & $venvPython manage.py seed_schemes
    Start-Process "http://localhost:8000/"
    & $venvPython manage.py runserver 0.0.0.0:8000
} else {
    Write-Host "[1/3] Using system Python..." -ForegroundColor Green
    python manage.py seed_schemes
    Start-Process "http://localhost:8000/"
    python manage.py runserver 0.0.0.0:8000
}
