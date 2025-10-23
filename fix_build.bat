@echo off
cd /d "%~dp0"
echo Fixing Python 3.12 compatibility...

echo Installing setuptools...
pip install setuptools

echo Cleaning build...
if exist build rmdir /s /q build

echo Building with compatibility fix...
python setup.py build

echo Build completed!
pause