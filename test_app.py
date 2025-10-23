"""
Quick test script to verify the alarm app works
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        print("  [OK] tkinter")
    except ImportError as e:
        print(f"  [ERROR] tkinter: {e}")
        return False
    
    try:
        import customtkinter as ctk
        print("  [OK] customtkinter")
    except ImportError as e:
        print(f"  [ERROR] customtkinter: {e}")
        print("  [FIX] Run: pip install customtkinter")
        return False
    
    try:
        import pygame
        print("  [OK] pygame")
    except ImportError as e:
        print(f"  [ERROR] pygame: {e}")
        print("  [FIX] Run: pip install pygame")
        return False
    
    try:
        from PIL import Image
        print("  [OK] Pillow")
    except ImportError as e:
        print(f"  [ERROR] Pillow: {e}")
        print("  [FIX] Run: pip install Pillow")
        return False
    
    try:
        import pystray
        print("  [OK] pystray")
    except ImportError as e:
        print(f"  [ERROR] pystray: {e}")
        print("  [FIX] Run: pip install pystray")
        return False
    
    return True

def test_assets():
    """Test if required assets exist"""
    print("\nTesting assets...")
    
    assets_ok = True
    
    # Check folders
    folders = ['assets', 'assets/logo', 'assets/ringtones', 'data']
    for folder in folders:
        if os.path.exists(folder):
            print(f"  [OK] {folder}/")
        else:
            print(f"  [ERROR] Missing folder: {folder}/")
            assets_ok = False
    
    # Check icon files
    icon_files = ['assets/logo/app_icon.ico', 'assets/logo/tray_icon.png']
    for icon_file in icon_files:
        if os.path.exists(icon_file):
            print(f"  [OK] {icon_file}")
        else:
            print(f"  [ERROR] Missing file: {icon_file}")
            print(f"  [FIX] Run: python create_icons.py")
            assets_ok = False
    
    return assets_ok

def main():
    print("RingRing Alarm App - Test Script")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test assets
    assets_ok = test_assets()
    
    print("\n" + "=" * 40)
    if imports_ok and assets_ok:
        print("[SUCCESS] All tests passed!")
        print("\nYou can now:")
        print("1. Run the app: python main.py")
        print("2. Build executable: build_app.bat")
        print("3. Create installer with Inno Setup")
    else:
        print("[ERROR] Some tests failed!")
        print("\nPlease fix the issues above before running the app.")
        
        if not imports_ok:
            print("\nTo install missing dependencies:")
            print("  pip install -r requirements.txt")

if __name__ == "__main__":
    main()