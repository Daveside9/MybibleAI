@echo off
REM MatchHang Quick Start Script (Windows)
REM This script sets up the development environment

echo.
echo ========================================
echo   MatchHang Quick Start (Windows)
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python 3.11+
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18+
    pause
    exit /b 1
)

echo [OK] Prerequisites check complete
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo [OK] Backend dependencies installed

REM Copy environment file
if not exist ".env" (
    copy .env.example .env
    echo [OK] .env file created (please edit with your credentials)
)

cd ..

REM Setup Frontend
echo.
echo Setting up Frontend...
cd frontend

REM Install dependencies
call npm install
echo [OK] Frontend dependencies installed

REM Copy environment file
if not exist ".env.local" (
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:4000
        echo NEXT_PUBLIC_SOCKET_URL=http://localhost:4000
        echo NEXT_PUBLIC_APP_NAME=MatchHang
        echo NEXT_PUBLIC_CURRENCY_SYMBOL=₦
        echo NEXT_PUBLIC_CHAT_UNLOCK_PRICE=100
        echo NEXT_PUBLIC_FREE_MESSAGES_PER_MATCH=3
    ) > .env.local
    echo [OK] .env.local file created
)

cd ..

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Setup PostgreSQL database:
echo    CREATE DATABASE matchhang;
echo    CREATE USER matchhang_user WITH PASSWORD 'your_password';
echo    GRANT ALL PRIVILEGES ON DATABASE matchhang TO matchhang_user;
echo.
echo 2. Update backend\.env with your database credentials
echo.
echo 3. Run database migrations:
echo    cd backend
echo    venv\Scripts\activate
echo    alembic upgrade head
echo.
echo 4. Start the backend:
echo    python main.py
echo.
echo 5. In a new terminal, start the frontend:
echo    cd frontend
echo    npm run dev
echo.
echo 6. Visit http://localhost:3000
echo.
echo Happy coding!
echo.
pause
