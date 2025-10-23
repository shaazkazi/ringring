@echo off
cd /d "%~dp0"
echo Building RingRing Alarm App...
echo.

echo Step 1: Installing Python dependencies...
pip install customtkinter==5.2.0
pip install pygame==2.5.2
pip install Pillow==10.0.1
pip install pystray==0.19.4
if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Step 2: Installing cx_Freeze for building executable...
pip install cx_Freeze
if %errorlevel% neq 0 (
    echo Failed to install cx_Freeze
    pause
    exit /b 1
)

echo Step 3: Building executable...
python setup.py build
if %errorlevel% neq 0 (
    echo Failed to build executable
    pause
    exit /b 1
)

echo Build completed successfully!
echo.
echo Your executable is located in: build\exe.win-amd64-3.11\
echo Main executable: build\exe.win-amd64-3.11\RingRing.exe
echo.
echo Next steps:
echo 1. Test the executable by running it from the build folder
echo 2. Use Inno Setup to create an installer (see instructions below)
echo.
pause