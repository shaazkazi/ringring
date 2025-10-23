@echo off
cd /d "%~dp0"
echo Installing RingRing Dependencies...
echo ===================================

echo.
echo Installing Python packages...
pip install customtkinter==5.2.0
pip install pygame==2.5.2
pip install Pillow==10.0.1
pip install pystray==0.19.4

echo.
echo Testing installation...
python test_app.py

echo.
echo Installation complete!
pause