@echo off
echo ========================================================
echo   Starting Yojana Mitra - Civic Eligibility Identifier
echo ========================================================
cd /d "%~dp0backend"

echo [1/3] Activating virtual environment...
if exist "..\venv\Scripts\activate.bat" (
    call "..\venv\Scripts\activate.bat"
) else (
    echo Virtual environment not found in ..\venv. Using system Python...
)

echo [2/3] Verifying and seeding government schemes...
python manage.py seed_schemes

echo [3/3] Launching Yojana Mitra at http://localhost:8000/
start "" "http://localhost:8000/"

python manage.py runserver 0.0.0.0:8000
pause
