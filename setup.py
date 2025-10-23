from cx_Freeze import setup, Executable
import sys
import os

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {
    'packages': ['tkinter', 'customtkinter', 'pygame', 'PIL', 'pystray', 'threading', 'json', 'datetime', 'distutils'],
    'excludes': [],
    'include_files': [
        ('assets/', 'assets/'),
        ('data/', 'data/') if os.path.exists('data') else None,
    ],
}

# Remove None entries
build_options['include_files'] = [f for f in build_options['include_files'] if f is not None]

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        'main.py',
        base=base,
        target_name='RingRing.exe',
        icon='assets/logo/app_icon.ico'
    )
]

setup(
    name='RingRing',
    version='1.0',
    description='Modern Alarm Clock Application',
    author='Your Name',
    options={'build_exe': build_options},
    executables=executables
)