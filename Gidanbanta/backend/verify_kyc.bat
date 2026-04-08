@echo off
echo ========================================
echo KYC Verification Tool
echo ========================================
echo.

if "%1"=="" (
    echo Usage: verify_kyc.bat ^<email^>
    echo Example: verify_kyc.bat user@example.com
    echo.
    echo To verify admin: verify_kyc.bat admin@matchhang.com
    pause
    exit /b 1
)

cd /d "%~dp0"
python verify_user_kyc.py %1
echo.
pause