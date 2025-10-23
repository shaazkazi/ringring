import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from datetime import datetime, timedelta
import threading
import time
import pygame
import json
import os
from PIL import Image, ImageTk
import pystray
from pystray import MenuItem as item
import sys
import traceback
import logging
import webbrowser

def setup_logging():
    logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def show_error_dialog(error_msg, full_traceback):
    error_window = ctk.CTkToplevel()
    error_window.title("Error - Ring Ring")
    error_window.geometry("600x400")
    error_window.attributes("-topmost", True)
    
    error_label = ctk.CTkLabel(error_window, text="An error occurred:", font=ctk.CTkFont(size=16, weight="bold"))
    error_label.pack(pady=10)
    
    error_text = ctk.CTkTextbox(error_window, height=250)
    error_text.pack(fill="both", expand=True, padx=20, pady=10)
    error_text.insert("1.0", f"Error: {error_msg}\n\nFull traceback:\n{full_traceback}")
    
    button_frame = ctk.CTkFrame(error_window)
    button_frame.pack(pady=10)
    
    def copy_error():
        error_window.clipboard_clear()
        error_window.clipboard_append(f"Error: {error_msg}\n\nFull traceback:\n{full_traceback}")
        messagebox.showinfo("Copied", "Error details copied to clipboard!")
    
    copy_btn = ctk.CTkButton(button_frame, text="Copy Error", command=copy_error)
    copy_btn.pack(side="left", padx=10)
    
    close_btn = ctk.CTkButton(button_frame, text="Close", command=error_window.destroy)
    close_btn.pack(side="left", padx=10)

class AlarmApp:
    def __init__(self):
        try:
            setup_logging()
            pygame.mixer.init()
            
            # Windows 11 style colors
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            self.root = ctk.CTk()
            self.root.title("Ring Ring")
            self.root.geometry("1000x750")
            self.root.minsize(900, 650)
            
            # Windows 11 style - rounded corners effect
            self.root.configure(corner_radius=12)
            
            try:
                self.root.iconbitmap("assets/logo/app_icon.ico")
            except:
                pass
            
            self.alarms = []
            self.running_alarms = {}
            self.is_minimized = False
            self.tray_icon = None
            
            self.load_settings()
            self.create_ui()
            self.load_alarms()
            
            self.alarm_thread = threading.Thread(target=self.check_alarms, daemon=True)
            self.alarm_thread.start()
            
            # Start countdown update thread
            self.countdown_thread = threading.Thread(target=self.countdown_updater, daemon=True)
            self.countdown_thread.start()
            
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        except Exception as e:
            error_msg = str(e)
            full_traceback = traceback.format_exc()
            logging.error(f"Initialization error: {error_msg}\n{full_traceback}")
            
            root = tk.Tk()
            root.withdraw()
            show_error_dialog(error_msg, full_traceback)
            root.mainloop()
    
    def create_ui(self):
        # Windows 11 style main container
        main_container = ctk.CTkFrame(self.root, corner_radius=0, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header with Windows 11 style
        header_frame = ctk.CTkFrame(main_container, height=70, corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title and theme toggle
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=15)
        
        title_label = ctk.CTkLabel(header_content, text="Ring Ring", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(side="left")
        
        # Countdown timer for next alarm
        self.countdown_label = ctk.CTkLabel(header_content, text="", font=ctk.CTkFont(size=14))
        self.countdown_label.pack(side="left", padx=(30, 0))
        
        # Windows 11 style theme toggle
        theme_container = ctk.CTkFrame(header_content, fg_color="transparent")
        theme_container.pack(side="right")
        
        self.theme_switch = ctk.CTkSwitch(
            theme_container, 
            text="Dark Mode", 
            font=ctk.CTkFont(size=12),
            command=self.toggle_theme,
            width=60,
            height=28
        )
        self.theme_switch.pack()
        
        # Start countdown timer
        self.update_countdown()
        
        # Navigation tabs - Windows 11 style
        nav_frame = ctk.CTkFrame(main_container, height=50, corner_radius=0)
        nav_frame.pack(fill="x", padx=0, pady=0)
        nav_frame.pack_propagate(False)
        
        self.notebook = ctk.CTkTabview(main_container, corner_radius=8)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        self.notebook.add("🏠 Alarms")
        self.notebook.add("➕ Add Alarm")
        self.notebook.add("⚙️ Settings")
        
        self.create_alarms_tab()
        self.create_add_alarm_tab()
        self.create_settings_tab()
    
    def create_alarms_tab(self):
        alarms_frame = self.notebook.tab("🏠 Alarms")
        
        # Header with Windows 11 card style
        header_card = ctk.CTkFrame(alarms_frame, height=60, corner_radius=12)
        header_card.pack(fill="x", padx=15, pady=(15, 10))
        header_card.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header_card, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=15)
        
        self.alarm_count_label = ctk.CTkLabel(header_content, text="No alarms", font=ctk.CTkFont(size=18, weight="bold"))
        self.alarm_count_label.pack(side="left")
        
        # Scrollable alarms list with Windows 11 style
        self.alarms_list_frame = ctk.CTkScrollableFrame(alarms_frame, corner_radius=12)
        self.alarms_list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.refresh_alarms_list()
    
    def create_add_alarm_tab(self):
        add_frame = self.notebook.tab("➕ Add Alarm")
        
        # Scrollable container for the form
        scroll_container = ctk.CTkScrollableFrame(add_frame, corner_radius=12)
        scroll_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Time selection card
        time_card = ctk.CTkFrame(scroll_container, corner_radius=12)
        time_card.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(time_card, text="⏰ Set Time", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 15))
        
        # Time selectors in a grid
        time_grid = ctk.CTkFrame(time_card, fg_color="transparent")
        time_grid.pack(pady=(0, 20))
        
        # Hour
        hour_container = ctk.CTkFrame(time_grid, corner_radius=8)
        hour_container.grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(hour_container, text="Hour", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        self.hour_var = tk.StringVar(value="12")
        self.hour_combo = ctk.CTkComboBox(hour_container, values=[f"{i:02d}" for i in range(1, 13)], variable=self.hour_var, width=100, height=40, font=ctk.CTkFont(size=14))
        self.hour_combo.pack(pady=(0, 10))
        
        # Minute
        minute_container = ctk.CTkFrame(time_grid, corner_radius=8)
        minute_container.grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkLabel(minute_container, text="Minute", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        self.minute_var = tk.StringVar(value="00")
        self.minute_combo = ctk.CTkComboBox(minute_container, values=[f"{i:02d}" for i in range(0, 60, 5)], variable=self.minute_var, width=100, height=40, font=ctk.CTkFont(size=14))
        self.minute_combo.pack(pady=(0, 10))
        
        # AM/PM
        ampm_container = ctk.CTkFrame(time_grid, corner_radius=8)
        ampm_container.grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkLabel(ampm_container, text="Period", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        self.ampm_var = tk.StringVar(value="AM")
        self.ampm_combo = ctk.CTkComboBox(ampm_container, values=["AM", "PM"], variable=self.ampm_var, width=100, height=40, font=ctk.CTkFont(size=14))
        self.ampm_combo.pack(pady=(0, 10))
        
        # Label card
        label_card = ctk.CTkFrame(scroll_container, corner_radius=12)
        label_card.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(label_card, text="📝 Alarm Label", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 15))
        self.label_entry = ctk.CTkEntry(label_card, placeholder_text="Enter alarm name...", height=45, font=ctk.CTkFont(size=14), corner_radius=8)
        self.label_entry.pack(fill="x", padx=20, pady=(0, 20))
        
        # Days card
        days_card = ctk.CTkFrame(scroll_container, corner_radius=12)
        days_card.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(days_card, text="📅 Repeat Days", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 15))
        
        days_grid = ctk.CTkFrame(days_card, fg_color="transparent")
        days_grid.pack(pady=(0, 20))
        
        self.days_vars = {}
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            var = tk.BooleanVar()
            self.days_vars[day] = var
            checkbox = ctk.CTkCheckBox(days_grid, text=day, variable=var, font=ctk.CTkFont(size=13), corner_radius=6)
            checkbox.grid(row=0, column=i, padx=8, pady=5)
        
        # Ringtone card
        ringtone_card = ctk.CTkFrame(scroll_container, corner_radius=12)
        ringtone_card.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(ringtone_card, text="🎵 Ringtone", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 15))
        
        ringtone_controls = ctk.CTkFrame(ringtone_card, fg_color="transparent")
        ringtone_controls.pack(pady=(0, 20))
        
        self.ringtone_var = tk.StringVar(value="Default")
        self.ringtone_combo = ctk.CTkComboBox(ringtone_controls, variable=self.ringtone_var, width=250, height=40, font=ctk.CTkFont(size=14))
        self.ringtone_combo.pack(side="left", padx=(0, 10))
        
        browse_btn = ctk.CTkButton(ringtone_controls, text="Browse", command=self.browse_ringtone, width=80, height=40, corner_radius=8)
        browse_btn.pack(side="left", padx=5)
        
        test_btn = ctk.CTkButton(ringtone_controls, text="Test", command=self.test_ringtone, width=60, height=40, corner_radius=8)
        test_btn.pack(side="left", padx=5)
        
        self.update_ringtone_list()
        
        # Add button - Windows 11 style
        add_btn = ctk.CTkButton(
            scroll_container, 
            text="➕ Add Alarm", 
            command=self.add_alarm, 
            font=ctk.CTkFont(size=16, weight="bold"), 
            height=50, 
            width=200,
            corner_radius=25
        )
        add_btn.pack(pady=20)
    
    def create_settings_tab(self):
        settings_frame = self.notebook.tab("⚙️ Settings")
        
        # Volume card
        volume_card = ctk.CTkFrame(settings_frame, corner_radius=12)
        volume_card.pack(fill="x", padx=15, pady=15)
        
        ctk.CTkLabel(volume_card, text="🔊 Volume", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 15))
        
        volume_container = ctk.CTkFrame(volume_card, fg_color="transparent")
        volume_container.pack(fill="x", padx=20, pady=(0, 20))
        
        self.volume_var = tk.DoubleVar(value=0.7)
        volume_slider = ctk.CTkSlider(volume_container, from_=0.0, to=1.0, variable=self.volume_var, command=self.change_volume, height=20, corner_radius=10)
        volume_slider.pack(fill="x", pady=(0, 10))
        
        self.volume_label = ctk.CTkLabel(volume_container, text="70%", font=ctk.CTkFont(size=14))
        self.volume_label.pack()
        
        # About card
        about_card = ctk.CTkFrame(settings_frame, corner_radius=12)
        about_card.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkLabel(about_card, text="ℹ️ About", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 15))
        
        about_content = ctk.CTkFrame(about_card, fg_color="transparent")
        about_content.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(about_content, text="Ring Ring", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 5))
        ctk.CTkLabel(about_content, text="Modern Alarm Clock App v1.0", font=ctk.CTkFont(size=14)).pack(pady=2)
        ctk.CTkLabel(about_content, text="Created with ❤️ by ShaazKazi", font=ctk.CTkFont(size=14)).pack(pady=2)
        
        github_btn = ctk.CTkButton(about_content, text="Visit GitHub", command=self.open_github, height=40, width=140, corner_radius=20)
        github_btn.pack(pady=15)
    
    def toggle_theme(self):
        if self.theme_switch.get():
            ctk.set_appearance_mode("light")
            self.theme_var = "light"
        else:
            ctk.set_appearance_mode("dark")
            self.theme_var = "dark"
        self.save_settings()
    
    def change_volume(self, value):
        pygame.mixer.music.set_volume(float(value))
        self.volume_label.configure(text=f"{int(float(value) * 100)}%")
        self.save_settings()
    
    def open_github(self):
        webbrowser.open("https://github.com/ShaazKazi")
    
    def update_ringtone_list(self):
        ringtones = ["Default"]
        ringtones_path = "assets/ringtones"
        if os.path.exists(ringtones_path):
            for file in os.listdir(ringtones_path):
                if file.endswith(('.mp3', '.wav', '.ogg')):
                    ringtones.append(file)
        self.ringtone_combo.configure(values=ringtones)
    
    def browse_ringtone(self):
        file_path = filedialog.askopenfilename(title="Select Ringtone", filetypes=[("Audio files", "*.mp3 *.wav *.ogg"), ("All files", "*.*")])
        if file_path:
            filename = os.path.basename(file_path)
            ringtones_path = "assets/ringtones"
            os.makedirs(ringtones_path, exist_ok=True)
            import shutil
            shutil.copy2(file_path, os.path.join(ringtones_path, filename))
            self.update_ringtone_list()
            self.ringtone_var.set(filename)
    
    def test_ringtone(self):
        ringtone = self.ringtone_var.get()
        self.play_alarm_sound(ringtone, test=True)
    
    def add_alarm(self):
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        ampm = self.ampm_var.get()
        
        if ampm == "PM" and hour != 12:
            hour += 12
        elif ampm == "AM" and hour == 12:
            hour = 0
        
        label = self.label_entry.get() or f"Alarm {hour:02d}:{minute:02d}"
        days = [day for day, var in self.days_vars.items() if var.get()]
        ringtone = self.ringtone_var.get()
        
        alarm = {
            "id": len(self.alarms),
            "hour": hour,
            "minute": minute,
            "label": label,
            "days": days,
            "ringtone": ringtone,
            "enabled": True,
            "created": datetime.now().isoformat()
        }
        
        self.alarms.append(alarm)
        self.save_alarms()
        self.refresh_alarms_list()
        self.update_countdown()  # Update countdown after adding alarm
        
        self.label_entry.delete(0, tk.END)
        for var in self.days_vars.values():
            var.set(False)
        
        messagebox.showinfo("Success", f"Alarm '{label}' added successfully!")
        self.notebook.set("🏠 Alarms")
    
    def refresh_alarms_list(self):
        for widget in self.alarms_list_frame.winfo_children():
            widget.destroy()
        
        count = len(self.alarms)
        self.alarm_count_label.configure(text=f"{count} alarm{'s' if count != 1 else ''}")
        
        if not self.alarms:
            # Windows 11 style empty state
            empty_card = ctk.CTkFrame(self.alarms_list_frame, height=250, corner_radius=12)
            empty_card.pack(fill="x", padx=10, pady=30)
            empty_card.pack_propagate(False)
            
            empty_content = ctk.CTkFrame(empty_card, fg_color="transparent")
            empty_content.pack(expand=True, fill="both")
            
            ctk.CTkLabel(empty_content, text="⏰", font=ctk.CTkFont(size=64)).pack(pady=(50, 15))
            ctk.CTkLabel(empty_content, text="No alarms set", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(0, 5))
            ctk.CTkLabel(empty_content, text="Add your first alarm to get started!", font=ctk.CTkFont(size=14)).pack()
            return
        
        for alarm in self.alarms:
            self.create_alarm_widget(alarm)
    
    def create_alarm_widget(self, alarm):
        # Windows 11 style alarm card with proper height
        alarm_card = ctk.CTkFrame(self.alarms_list_frame, height=140, corner_radius=12)
        alarm_card.pack(fill="x", padx=10, pady=8)
        alarm_card.pack_propagate(False)
        
        card_content = ctk.CTkFrame(alarm_card, fg_color="transparent")
        card_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Time display - fixed width
        time_container = ctk.CTkFrame(card_content, width=130, corner_radius=8)
        time_container.pack(side="left", fill="y", padx=(0, 20))
        time_container.pack_propagate(False)
        
        display_hour = alarm['hour']
        ampm = "AM"
        if display_hour == 0:
            display_hour = 12
        elif display_hour > 12:
            display_hour -= 12
            ampm = "PM"
        elif display_hour == 12:
            ampm = "PM"
        
        time_str = f"{display_hour:02d}:{alarm['minute']:02d}"
        time_label = ctk.CTkLabel(time_container, text=time_str, font=ctk.CTkFont(size=24, weight="bold"))
        time_label.pack(pady=(20, 5))
        
        ampm_label = ctk.CTkLabel(time_container, text=ampm, font=ctk.CTkFont(size=12))
        ampm_label.pack()
        
        # Details - expandable
        details_container = ctk.CTkFrame(card_content, corner_radius=8)
        details_container.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        details_content = ctk.CTkFrame(details_container, fg_color="transparent")
        details_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Truncate long labels
        label_text = alarm['label']
        if len(label_text) > 25:
            label_text = label_text[:22] + "..."
        
        label_widget = ctk.CTkLabel(details_content, text=label_text, font=ctk.CTkFont(size=15, weight="bold"), anchor="w")
        label_widget.pack(fill="x", pady=(0, 8))
        
        if alarm['days']:
            days_text = f"Repeats: {', '.join(alarm['days'])}"
            if len(days_text) > 30:
                days_text = days_text[:27] + "..."
            days_widget = ctk.CTkLabel(details_content, text=days_text, font=ctk.CTkFont(size=11), anchor="w")
        else:
            days_widget = ctk.CTkLabel(details_content, text="One-time alarm", font=ctk.CTkFont(size=11), anchor="w")
        days_widget.pack(fill="x", pady=2)
        
        ringtone_text = f"🎵 {alarm['ringtone']}"
        if len(ringtone_text) > 25:
            ringtone_text = ringtone_text[:22] + "..."
        ringtone_widget = ctk.CTkLabel(details_content, text=ringtone_text, font=ctk.CTkFont(size=11), anchor="w")
        ringtone_widget.pack(fill="x", pady=2)
        
        # Controls - side by side layout
        controls_container = ctk.CTkFrame(card_content, width=140, corner_radius=8)
        controls_container.pack(side="right", fill="y")
        controls_container.pack_propagate(False)
        
        controls_content = ctk.CTkFrame(controls_container, fg_color="transparent")
        controls_content.pack(fill="both", expand=True, padx=15, pady=20)
        
        # Toggle and Delete in same row
        controls_row = ctk.CTkFrame(controls_content, fg_color="transparent")
        controls_row.pack(expand=True)
        
        enabled_var = tk.BooleanVar(value=alarm['enabled'])
        enabled_switch = ctk.CTkSwitch(controls_row, text="", variable=enabled_var, command=lambda: self.toggle_alarm(alarm['id'], enabled_var.get()), width=50)
        enabled_switch.pack(pady=(0, 15))
        
        delete_btn = ctk.CTkButton(controls_row, text="Delete", command=lambda: self.delete_alarm(alarm['id']), width=90, height=32, fg_color="#dc3545", hover_color="#c82333", corner_radius=8, font=ctk.CTkFont(size=12))
        delete_btn.pack()
    
    def toggle_alarm(self, alarm_id, enabled):
        for alarm in self.alarms:
            if alarm['id'] == alarm_id:
                alarm['enabled'] = enabled
                break
        self.save_alarms()
        self.update_countdown()  # Update countdown when toggling alarm
    
    def delete_alarm(self, alarm_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this alarm?"):
            self.alarms = [alarm for alarm in self.alarms if alarm['id'] != alarm_id]
            self.save_alarms()
            self.refresh_alarms_list()
            self.update_countdown()  # Update countdown after deleting alarm
    
    def check_alarms(self):
        while True:
            current_time = datetime.now()
            current_day = current_time.strftime("%a")
            
            for alarm in self.alarms:
                if not alarm['enabled']:
                    continue
                
                if (current_time.hour == alarm['hour'] and current_time.minute == alarm['minute'] and current_time.second == 0):
                    if not alarm['days'] or current_day in alarm['days']:
                        if alarm['id'] not in self.running_alarms:
                            self.trigger_alarm(alarm)
            
            time.sleep(1)
    
    def trigger_alarm(self, alarm):
        self.running_alarms[alarm['id']] = True
        self.show_alarm_popup(alarm)
        sound_thread = threading.Thread(target=self.play_alarm_sound, args=(alarm['ringtone'],), daemon=True)
        sound_thread.start()
    
    def show_alarm_popup(self, alarm):
        popup = ctk.CTkToplevel(self.root)
        popup.title("⏰ ALARM - Ring Ring")
        popup.geometry("500x400")
        popup.attributes("-topmost", True)
        popup.grab_set()
        popup.configure(corner_radius=12)
        
        # Set proper icon for popup
        try:
            if os.path.exists("assets/logo/app_icon.ico"):
                popup.iconbitmap("assets/logo/app_icon.ico")
            else:
                popup.iconbitmap(default="assets/logo/app_icon.ico")
        except Exception as e:
            print(f"Icon error: {e}")
            try:
                popup.wm_iconbitmap("assets/logo/app_icon.ico")
            except:
                pass
        
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - (popup.winfo_width() // 2)
        y = (popup.winfo_screenheight() // 2) - (popup.winfo_height() // 2)
        popup.geometry(f"+{x}+{y}")
        
        # Windows 11 style popup content
        content_frame = ctk.CTkFrame(popup, corner_radius=12)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        alarm_icon = ctk.CTkLabel(content_frame, text="⏰", font=ctk.CTkFont(size=80))
        alarm_icon.pack(pady=(40, 20))
        
        display_hour = alarm['hour']
        ampm = "AM"
        if display_hour == 0:
            display_hour = 12
        elif display_hour > 12:
            display_hour -= 12
            ampm = "PM"
        elif display_hour == 12:
            ampm = "PM"
        
        time_label = ctk.CTkLabel(content_frame, text=f"{display_hour:02d}:{alarm['minute']:02d} {ampm}", font=ctk.CTkFont(size=36, weight="bold"))
        time_label.pack(pady=10)
        
        label_text = ctk.CTkLabel(content_frame, text=alarm['label'], font=ctk.CTkFont(size=18))
        label_text.pack(pady=10)
        
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(pady=30)
        
        # Buttons side by side with proper spacing
        buttons_container = ctk.CTkFrame(button_frame, fg_color="transparent")
        buttons_container.pack()
        
        stop_btn = ctk.CTkButton(buttons_container, text="Stop", command=lambda: self.stop_alarm(alarm['id'], popup), width=130, height=45, font=ctk.CTkFont(size=15, weight="bold"), corner_radius=22)
        stop_btn.pack(side="left", padx=10)
        
        snooze_btn = ctk.CTkButton(buttons_container, text="Snooze (5 min)", command=lambda: self.snooze_alarm(alarm, popup), width=150, height=45, font=ctk.CTkFont(size=15, weight="bold"), corner_radius=22)
        snooze_btn.pack(side="left", padx=10)
    
    def stop_alarm(self, alarm_id, popup):
        pygame.mixer.music.stop()
        if alarm_id in self.running_alarms:
            del self.running_alarms[alarm_id]
        popup.destroy()
    
    def snooze_alarm(self, alarm, popup):
        pygame.mixer.music.stop()
        if alarm['id'] in self.running_alarms:
            del self.running_alarms[alarm['id']]
        popup.destroy()
        
        snooze_time = datetime.now() + timedelta(minutes=5)
        snooze_alarm = alarm.copy()
        snooze_alarm['id'] = f"snooze_{alarm['id']}_{int(time.time())}"
        snooze_alarm['hour'] = snooze_time.hour
        snooze_alarm['minute'] = snooze_time.minute
        snooze_alarm['label'] = f"Snooze: {alarm['label']}"
        snooze_alarm['days'] = []
        
        self.alarms.append(snooze_alarm)
    
    def play_alarm_sound(self, ringtone, test=False):
        try:
            if ringtone == "Default":
                for _ in range(10 if not test else 3):
                    import winsound
                    winsound.Beep(1000, 500)
                    if test:
                        break
                    time.sleep(0.5)
            else:
                ringtone_path = os.path.join("assets/ringtones", ringtone)
                if os.path.exists(ringtone_path):
                    pygame.mixer.music.load(ringtone_path)
                    pygame.mixer.music.set_volume(self.volume_var.get())
                    if test:
                        pygame.mixer.music.play()
                        time.sleep(3)
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error playing sound: {e}")
    
    def minimize_to_tray(self):
        self.root.withdraw()
        self.is_minimized = True
        
        try:
            image = Image.open("assets/logo/tray_icon.png")
        except:
            image = Image.new('RGB', (64, 64), color='blue')
        
        menu = pystray.Menu(item('Show', self.show_from_tray), item('Quit', self.quit_app))
        self.tray_icon = pystray.Icon("Ring Ring", image, "Ring Ring Alarm", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def show_from_tray(self):
        self.root.deiconify()
        self.root.lift()
        self.is_minimized = False
        if self.tray_icon:
            self.tray_icon.stop()
    
    def on_closing(self):
        if messagebox.askyesno("Minimize to Tray", "Do you want to minimize to system tray instead of closing?"):
            self.minimize_to_tray()
        else:
            self.quit_app()
    
    def quit_app(self):
        self.save_settings()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        sys.exit()
    
    def save_alarms(self):
        os.makedirs("data", exist_ok=True)
        with open("data/alarms.json", "w") as f:
            json.dump(self.alarms, f, indent=2)
    
    def load_alarms(self):
        try:
            with open("data/alarms.json", "r") as f:
                self.alarms = json.load(f)
        except FileNotFoundError:
            self.alarms = []
    
    def save_settings(self):
        settings = {"theme": getattr(self, 'theme_var', 'dark'), "volume": self.volume_var.get()}
        os.makedirs("data", exist_ok=True)
        with open("data/settings.json", "w") as f:
            json.dump(settings, f, indent=2)
    
    def load_settings(self):
        try:
            with open("data/settings.json", "r") as f:
                settings = json.load(f)
                self.theme_var = settings.get("theme", "dark")
                if hasattr(self, 'volume_var'):
                    self.volume_var.set(settings.get("volume", 0.7))
                if hasattr(self, 'theme_switch'):
                    self.theme_switch.set(self.theme_var == "light")
        except FileNotFoundError:
            self.theme_var = "dark"
    
    def get_next_alarm(self):
        """Get the next upcoming alarm"""
        if not self.alarms:
            return None
        
        now = datetime.now()
        upcoming_alarms = []
        
        for alarm in self.alarms:
            if not alarm['enabled']:
                continue
            
            # Calculate next occurrence
            alarm_time = now.replace(hour=alarm['hour'], minute=alarm['minute'], second=0, microsecond=0)
            
            if alarm['days']:  # Recurring alarm
                days_map = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}
                current_weekday = now.weekday()
                
                for day in alarm['days']:
                    day_num = days_map[day]
                    days_ahead = (day_num - current_weekday) % 7
                    
                    if days_ahead == 0:  # Today
                        if alarm_time > now:
                            upcoming_alarms.append((alarm_time, alarm))
                        else:
                            # Next week
                            next_week = alarm_time + timedelta(days=7)
                            upcoming_alarms.append((next_week, alarm))
                    else:
                        next_occurrence = alarm_time + timedelta(days=days_ahead)
                        upcoming_alarms.append((next_occurrence, alarm))
            else:  # One-time alarm
                if alarm_time > now:
                    upcoming_alarms.append((alarm_time, alarm))
                else:
                    # Tomorrow
                    tomorrow = alarm_time + timedelta(days=1)
                    upcoming_alarms.append((tomorrow, alarm))
        
        if upcoming_alarms:
            return min(upcoming_alarms, key=lambda x: x[0])
        return None
    
    def update_countdown(self):
        """Update countdown display"""
        next_alarm = self.get_next_alarm()
        if next_alarm:
            alarm_time, alarm = next_alarm
            now = datetime.now()
            time_diff = alarm_time - now
            
            if time_diff.total_seconds() > 0:
                hours = int(time_diff.total_seconds() // 3600)
                minutes = int((time_diff.total_seconds() % 3600) // 60)
                
                if hours > 24:
                    days = hours // 24
                    hours = hours % 24
                    countdown_text = f"⏳ Next: {alarm['label']} in {days}d {hours}h {minutes}m"
                elif hours > 0:
                    countdown_text = f"⏳ Next: {alarm['label']} in {hours}h {minutes}m"
                else:
                    countdown_text = f"⏳ Next: {alarm['label']} in {minutes}m"
                
                if hasattr(self, 'countdown_label'):
                    self.countdown_label.configure(text=countdown_text)
            else:
                if hasattr(self, 'countdown_label'):
                    self.countdown_label.configure(text="")
        else:
            if hasattr(self, 'countdown_label'):
                self.countdown_label.configure(text="")
    
    def countdown_updater(self):
        """Background thread to update countdown every minute"""
        while True:
            try:
                self.update_countdown()
                time.sleep(60)  # Update every minute
            except:
                break
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = AlarmApp()
        app.run()
    except Exception as e:
        error_msg = str(e)
        full_traceback = traceback.format_exc()
        
        try:
            logging.error(f"Main error: {error_msg}\n{full_traceback}")
        except:
            pass
        
        try:
            root = tk.Tk()
            root.withdraw()
            show_error_dialog(error_msg, full_traceback)
            root.mainloop()
        except:
            print(f"CRITICAL ERROR: {error_msg}")
            print(f"Full traceback:\n{full_traceback}")
            input("Press Enter to exit...")