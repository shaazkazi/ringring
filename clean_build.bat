@echo off
cd /d "%~dp0"
echo Cleaning build cache...

if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__

echo Clean build with custom icon...
python setup.py build

echo Build completed!
echo Your executable: build\exe.win-amd64-3.12\RingRing.exe
pause