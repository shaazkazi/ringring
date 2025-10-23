# 🚀 RingRing Setup Guide

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
install_dependencies.bat
```

### Step 2: Run the App
```bash
python main.py
```

### Step 3: Build Executable (Optional)
```bash
build_app.bat
```

## 📋 Complete Setup Instructions

### 1. Prerequisites
- **Python 3.11+** installed from [python.org](https://python.org)
- **Windows 10/11**

### 2. Install & Test
1. **Double-click**: `install_dependencies.bat`
2. **Wait for completion** (installs all required packages)
3. **Check results** (test script runs automatically)

### 3. Run the App
1. **Double-click**: `main.py` OR
2. **Command line**: `python main.py`

### 4. Using the App

#### Adding Alarms:
1. Click **"➕ Add Alarm"** tab
2. Set time using dropdowns
3. Enter alarm name
4. Select repeat days (optional)
5. Choose ringtone
6. Click **"➕ Add Alarm"**

#### Managing Alarms:
- **Enable/Disable**: Toggle switch on each alarm
- **Delete**: Click 🗑️ button
- **View All**: Check **"⏰ Alarms"** tab

#### System Tray:
- **Minimize**: Close window → Choose "Minimize to Tray"
- **Show**: Right-click tray icon → "Show"
- **Quit**: Right-click tray icon → "Quit"

#### Settings:
- **Theme**: Dark/Light mode in **"⚙️ Settings"**
- **Volume**: Adjust alarm volume slider
- **Ringtones**: Add MP3/WAV files to `assets/ringtones/`

### 5. Build Executable

#### Method 1: Automatic
```bash
build_app.bat
```

#### Method 2: Manual
```bash
pip install cx_Freeze
python setup.py build
```

**Result**: `build\exe.win-amd64-3.11\RingRing.exe`

### 6. Create Windows Installer

#### Install Inno Setup:
1. Download from: https://jrsoftware.org/isinfo.php
2. Install with default settings

#### Create Installer:
1. **Build executable first** (Step 5)
2. **Open Inno Setup Compiler**
3. **File** → **Open** → Select `installer.iss`
4. **Press F9** or **Build** → **Compile**
5. **Find installer**: `installer_output\RingRing_Setup.exe`

## 🎨 Customization

### App Icon:
1. **Replace**: `assets/logo/app_icon.ico`
2. **Or modify**: `create_icons.py` script
3. **Rebuild**: Run `build_app.bat`

### Ringtones:
1. **Add files**: Copy MP3/WAV to `assets/ringtones/`
2. **Or use app**: Browse button in Add Alarm tab
3. **Supported**: MP3, WAV, OGG formats

### Colors/Theme:
Edit `main.py`:
```python
# Line 15-16
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
```

## 🔧 Troubleshooting

### "Module not found":
```bash
pip install -r requirements.txt
```

### "Permission denied":
- Run Command Prompt as Administrator
- Or install Python with "Add to PATH" option

### App won't start:
1. Run: `python test_app.py`
2. Fix any reported issues
3. Try again

### No sound:
- Check Windows volume
- Verify audio files in `assets/ringtones/`
- Test with "Default" ringtone first

### Build fails:
- Ensure Python 3.11+ installed
- Run `pip install cx_Freeze`
- Check all dependencies installed

## 📁 File Structure

```
ringring/
├── main.py                    # 🎯 Main app (run this)
├── install_dependencies.bat   # 📦 Install packages
├── build_app.bat             # 🏗️ Build executable
├── test_app.py               # 🧪 Test everything works
├── requirements.txt          # 📋 Python packages needed
├── setup.py                  # ⚙️ Build configuration
├── installer.iss             # 📦 Inno Setup script
├── assets/
│   ├── logo/
│   │   ├── app_icon.ico      # 🎨 Main app icon
│   │   └── tray_icon.png     # 🔔 System tray icon
│   └── ringtones/            # 🎵 Add your MP3/WAV files here
└── data/                     # 💾 App saves alarms/settings here
```

## 🎯 Quick Commands

| Action | Command |
|--------|---------|
| Install everything | `install_dependencies.bat` |
| Run app | `python main.py` |
| Test setup | `python test_app.py` |
| Build exe | `build_app.bat` |
| Create icons | `python create_icons.py` |

---

**Need help?** Check the main README.md for detailed information!