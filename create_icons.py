from PIL import Image, ImageDraw
import os

def create_app_icon():
    """Create a modern alarm clock icon"""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw clock circle
    margin = 20
    circle_bbox = [margin, margin, size-margin, size-margin]
    
    # Outer circle (dark)
    draw.ellipse(circle_bbox, fill='#2B2B2B', outline='#4A9EFF', width=8)
    
    # Inner circle (lighter)
    inner_margin = 40
    inner_bbox = [inner_margin, inner_margin, size-inner_margin, size-inner_margin]
    draw.ellipse(inner_bbox, fill='#3B3B3B')
    
    # Clock hands
    center = size // 2
    
    # Hour hand (shorter, thicker)
    hour_length = 60
    draw.line([center, center, center, center-hour_length], fill='#4A9EFF', width=8)
    
    # Minute hand (longer, thinner)
    minute_length = 80
    draw.line([center, center, center+minute_length//1.5, center], fill='#4A9EFF', width=6)
    
    # Center dot
    dot_size = 12
    dot_bbox = [center-dot_size//2, center-dot_size//2, center+dot_size//2, center+dot_size//2]
    draw.ellipse(dot_bbox, fill='#FF6B6B')
    
    # Hour markers
    for i in range(12):
        angle = i * 30  # 360/12 = 30 degrees per hour
        import math
        x1 = center + (size//2 - 60) * math.cos(math.radians(angle - 90))
        y1 = center + (size//2 - 60) * math.sin(math.radians(angle - 90))
        x2 = center + (size//2 - 45) * math.cos(math.radians(angle - 90))
        y2 = center + (size//2 - 45) * math.sin(math.radians(angle - 90))
        draw.line([x1, y1, x2, y2], fill='#FFFFFF', width=3)
    
    # Save as ICO for Windows
    img.save('assets/logo/app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    # Save as PNG for tray icon
    tray_img = img.resize((64, 64), Image.Resampling.LANCZOS)
    tray_img.save('assets/logo/tray_icon.png')
    
    print("[SUCCESS] App icons created successfully!")

def create_sample_ringtones_info():
    """Create info file about adding ringtones"""
    info_text = """RINGTONES FOLDER
    
Place your custom ringtone files here!

Supported formats:
- MP3 (.mp3)
- WAV (.wav) 
- OGG (.ogg)

How to add ringtones:
1. Copy your audio files to this folder
2. Or use the "Browse" button in the app to select and copy files
3. The app will automatically detect new ringtones

Sample ringtones you can download:
- Classic alarm sounds
- Nature sounds (birds, rain, ocean)
- Gentle wake-up melodies
- Custom music tracks

Note: Keep file sizes reasonable (under 10MB) for best performance.
"""
    
    with open('assets/ringtones/README.txt', 'w') as f:
        f.write(info_text)
    
    print("[SUCCESS] Ringtones info created!")

if __name__ == "__main__":
    create_app_icon()
    create_sample_ringtones_info()
    print("\n[SUCCESS] All assets created successfully!")
    print("[INFO] Folder structure:")
    print("   assets/")
    print("   +-- logo/")
    print("   |   +-- app_icon.ico")
    print("   |   +-- tray_icon.png")
    print("   +-- ringtones/")
    print("       +-- README.txt")