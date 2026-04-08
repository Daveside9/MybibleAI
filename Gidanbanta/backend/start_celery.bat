@echo off
echo Starting Celery Worker with Beat Scheduler...
echo.
echo Make sure Redis is running on localhost:6379
echo.

cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Start Celery worker with beat
python run_celery.py

pause
