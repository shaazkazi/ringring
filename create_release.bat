@echo off
echo Creating Ring Ring Release Package...
echo =====================================

echo.
echo Checking for installer...
if exist "installer_output\Ring_Ring_Setup.exe" (
    echo [SUCCESS] Found installer: Ring_Ring_Setup.exe
    echo.
    echo File details:
    dir "installer_output\Ring_Ring_Setup.exe"
    echo.
    echo [READY FOR RELEASE]
    echo Your installer is ready at: installer_output\Ring_Ring_Setup.exe
    echo.
    echo This is the file you can:
    echo - Send to users for installation
    echo - Upload to GitHub releases
    echo - Distribute as software installer
    echo.
    echo The installer will:
    echo - Install Ring Ring to Program Files
    echo - Create desktop shortcut
    echo - Add to Start Menu
    echo - Option to start with Windows
    echo.
) else (
    echo [ERROR] Installer not found!
    echo Please run Inno Setup first:
    echo 1. Open Inno Setup Compiler
    echo 2. Open installer.iss
    echo 3. Press F9 to compile
    echo.
)

echo.
echo Press any key to open installer folder...
pause >nul
explorer installer_output