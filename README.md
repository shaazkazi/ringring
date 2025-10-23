# 🔔 RingRing - Modern Alarm Clock App

A beautiful, modern alarm clock application for Windows with a minimalistic design and powerful features.

## ✨ Features

- 🎨 **Modern UI**: Beautiful dark/light theme with customizable appearance
- ⏰ **Multiple Alarms**: Set unlimited alarms with custom labels
- 🔄 **Recurring Alarms**: Set alarms for specific days of the week
- 🎵 **Custom Ringtones**: Use your own MP3/WAV files or built-in sounds
- 🔊 **Volume Control**: Adjustable alarm volume
- 📱 **System Tray**: Minimize to system tray and run in background
- ⏸️ **Snooze Function**: 5-minute snooze option
- 💾 **Auto-Save**: All settings and alarms are automatically saved

## 🚀 Quick Start

### Option 1: Run from Source (Recommended for Development)

1. **Install Python 3.11+** from [python.org](https://python.org)

2. **Clone/Download** this project to your computer

3. **Run the build script**:
   ```bash
   build_app.bat
   ```

4. **Run the app**:
   ```bash
   python main.py
   ```

### Option 2: Build Executable

1. **Run the build script**:
   ```bash
   build_app.bat
   ```

2. **Find your executable** in:
   ```
   build\exe.win-amd64-3.11\RingRing.exe
   ```

## 📦 Creating Windows Installer with Inno Setup

### Step 1: Install Inno Setup
1. Download **Inno Setup** from: https://jrsoftware.org/isinfo.php
2. Install it with default settings

### Step 2: Create Installer
1. **Build the executable first** using `build_app.bat`
2. **Open Inno Setup Compiler**
3. **Open the script**: `File` → `Open` → Select `installer.iss`
4. **Compile**: Press `F9` or `Build` → `Compile`
5. **Find installer**: Check `installer_output\RingRing_Setup.exe`

### Step 3: Customize Installer (Optional)
Edit `installer.iss` to customize:
- **App name and version** (lines 2-3)
- **Publisher info** (lines 4-6)
- **Installation directory** (line 7)
- **License file** (line 11)
- **App icon** (line 15)

## 📁 Project Structure

```
ringring/
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── setup.py               # Build configuration
├── installer.iss          # Inno Setup script
├── build_app.bat          # Build automation script
├── create_icons.py        # Icon generation script
├── assets/
│   ├── logo/
│   │   ├── app_icon.ico   # Main app icon (auto-generated)
│   │   └── tray_icon.png  # System tray icon (auto-generated)
│   └── ringtones/
│       └── README.txt     # Instructions for adding ringtones
└── data/
    ├── alarms.json        # Saved alarms (auto-created)
    └── settings.json      # App settings (auto-created)
```

## 🎵 Adding Custom Ringtones

1. **Supported formats**: MP3, WAV, OGG
2. **Add ringtones**:
   - Copy files to `assets/ringtones/` folder, OR
   - Use the "Browse" button in the app
3. **File size**: Keep under 10MB for best performance

## 🎨 Customizing App Icon

### Replace the Default Icon:
1. **Create your icon** (256x256 PNG recommended)
2. **Convert to ICO format** using online tools or:
   ```bash
   python create_icons.py  # Modify this script
   ```
3. **Replace**: `assets/logo/app_icon.ico`
4. **Rebuild** the app

### Icon Requirements:
- **Format**: ICO file with multiple sizes (16x16 to 256x256)
- **Background**: Transparent recommended
- **Style**: Simple, recognizable at small sizes

## ⚙️ Configuration

### Theme Customization
Edit `main.py` to change colors:
```python
# Line 15-16: Change default theme
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
```

### Default Settings
Modify default values in `main.py`:
- **Volume**: Line 45 `self.volume_var = tk.DoubleVar(value=0.7)`
- **Theme**: Line 15 `ctk.set_appearance_mode("dark")`

## 🔧 Troubleshooting

### Common Issues:

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**Icon not showing:**
- Ensure `assets/logo/app_icon.ico` exists
- Run `python create_icons.py` to generate icons

**Audio not playing:**
- Check if pygame is installed: `pip install pygame`
- Verify ringtone file format (MP3/WAV/OGG)
- Check Windows audio settings

**Build fails:**
- Ensure Python 3.11+ is installed
- Run as Administrator if needed
- Check all dependencies are installed

### System Requirements:
- **OS**: Windows 10/11
- **Python**: 3.11 or higher
- **RAM**: 100MB minimum
- **Storage**: 50MB for app + ringtones

## 🚀 Advanced Usage

### Running at Startup:
The installer includes an option to start RingRing automatically with Windows.

### Command Line Options:
```bash
python main.py --minimized    # Start minimized to tray
```

### Backup/Restore Alarms:
- **Backup**: Copy `data/alarms.json`
- **Restore**: Replace `data/alarms.json` with backup

## 📝 License

This project is open source. Feel free to modify and distribute.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Try rebuilding the app
4. Check Windows compatibility

---

**Enjoy your new modern alarm clock! ⏰✨**