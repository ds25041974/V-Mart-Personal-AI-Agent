@echo off
REM V-Mart Personal AI Agent - Windows Installer Launcher
REM This script launches the PowerShell installer with proper execution policy

title V-Mart AI Agent Installer

echo ========================================
echo   V-Mart Personal AI Agent Installer
echo   Windows 10/11
echo ========================================
echo.

REM Check if PowerShell is available
powershell -Command "Write-Host 'PowerShell detected'" >nul 2>&1
if errorlevel 1 (
    echo ERROR: PowerShell not found!
    echo PowerShell is required to run this installer.
    echo.
    pause
    exit /b 1
)

echo Starting installer...
echo.

REM Run PowerShell installer with bypass execution policy
powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1"

if errorlevel 1 (
    echo.
    echo Installation failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

exit /b 0
