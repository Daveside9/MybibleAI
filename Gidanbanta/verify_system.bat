@echo off
echo ========================================
echo MatchHang System Verification
echo ========================================
echo.

echo Checking backend...
curl -s http://localhost:4000/health >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Backend is running
) else (
    echo [ERROR] Backend is NOT running
    echo        Run: cd backend ^&^& python main.py
)

echo.
echo Checking frontend...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Frontend is running
) else (
    echo [ERROR] Frontend is NOT running
    echo        Run: cd frontend ^&^& npm run dev
)

echo.
echo Checking database...
cd backend
python -c "import sqlite3; conn = sqlite3.connect('matchhang.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM matches'); print(f'[OK] Database has {cursor.fetchone()[0]} matches'); conn.close()" 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Database check failed
)
cd ..

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Make sure both backend and frontend are running
echo 2. Open http://localhost:3000 in your browser
echo 3. Press F12 to open DevTools
echo 4. Clear Local Storage (Application tab)
echo 5. Login and watch Console for debug logs
echo.
echo For detailed help, see SOLUTION.md
echo ========================================
pause
