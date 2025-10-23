@echo off
cd /d "%~dp0"
echo Building with PyInstaller...

echo Installing PyInstaller...
pip install pyinstaller

echo Building executable...
pyinstaller --onefile --windowed --icon=assets/logo/app_icon.ico --add-data "assets;assets" --add-data "data;data" --name RingRing main.py

echo Build completed!
echo Your executable: dist\RingRing.exe
pause