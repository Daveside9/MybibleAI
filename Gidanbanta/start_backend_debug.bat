@echo off
echo ========================================
echo Starting Backend with Debug Output
echo ========================================
echo.

cd backend

echo Activating virtual environment...
call .\venv\Scripts\activate.bat

echo.
echo Starting backend on http://localhost:4000
echo Press Ctrl+C to stop
echo.

python main.py

echo.
echo Backend stopped.
pause
