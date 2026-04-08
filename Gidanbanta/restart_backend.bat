@echo off
echo ========================================
echo Restarting Backend with Fresh Config
echo ========================================
echo.

cd backend

echo Stopping any running Python processes...
taskkill /F /IM python.exe 2>nul

echo.
echo Starting backend...
echo.

.\venv\Scripts\python.exe main.py

pause
