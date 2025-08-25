import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import random
import pyautogui
import keyboard
import win32gui
import win32con
import win32process
import sys
from datetime import datetime

class WoWBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WoW Bot - Multiple Windows")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
        
        # Dark theme colors
        self.colors = {
            'bg_dark': '#1a1a1a',
            'bg_medium': '#2d2d2d',
            'bg_light': '#3d3d3d',
            'accent_blue': '#4a9eff',
            'accent_green': '#00d4aa',
            'accent_red': '#ff6b6b',
            'accent_orange': '#ffa726',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'text_muted': '#808080',
            'border': '#404040'
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Bot state
        self.bot_running = False
        self.bot_thread = None
        self.wow_windows = []
        self.selected_windows = []
        self.current_window_index = 0
        self.base_interval = 2.0
        self.random_range = 10.0
        
        # Configure style
        self.setup_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Auto-detect windows on startup
        self.detect_windows()
    
    def setup_styles(self):
        """Configure modern dark theme styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure frame styles
        style.configure('Dark.TFrame', background=self.colors['bg_dark'])
        style.configure('Medium.TFrame', background=self.colors['bg_medium'])
        style.configure('Light.TFrame', background=self.colors['bg_light'])
        
        # Configure label styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 20, 'bold'), 
                       foreground=self.colors['accent_blue'],
                       background=self.colors['bg_dark'])
        
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_medium'])
        
        style.configure('Status.TLabel', 
                       font=('Segoe UI', 10), 
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_medium'])
        
        style.configure('Success.TLabel', 
                       font=('Segoe UI', 10, 'bold'), 
                       foreground=self.colors['accent_green'],
                       background=self.colors['bg_medium'])
        
        style.configure('Error.TLabel', 
                       font=('Segoe UI', 10, 'bold'), 
                       foreground=self.colors['accent_red'],
                       background=self.colors['bg_medium'])
        
        # Configure button styles
        style.configure('Start.TButton', 
                       font=('Segoe UI', 11, 'bold'), 
                       foreground=self.colors['text_primary'],
                       background=self.colors['accent_green'])
        
        style.configure('Stop.TButton', 
                       font=('Segoe UI', 11, 'bold'), 
                       foreground=self.colors['text_primary'],
                       background=self.colors['accent_red'])
        
        style.configure('Config.TButton', 
                       font=('Segoe UI', 10), 
                       foreground=self.colors['text_primary'],
                       background=self.colors['accent_blue'])
        
        style.configure('Emergency.TButton', 
                       font=('Segoe UI', 10, 'bold'), 
                       foreground=self.colors['text_primary'],
                       background=self.colors['accent_orange'])
        
        # Configure labelframe styles
        style.configure('Dark.TLabelframe', 
                       background=self.colors['bg_medium'],
                       bordercolor=self.colors['border'])
        
        style.configure('Dark.TLabelframe.Label', 
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['accent_blue'],
                       background=self.colors['bg_medium'])
        
        # Configure progressbar
        style.configure('Dark.Horizontal.TProgressbar',
                       background=self.colors['accent_blue'],
                       troughcolor=self.colors['bg_light'],
                       bordercolor=self.colors['border'])
    
    def create_widgets(self):
        """Create all GUI widgets with dark theme"""
        # Create main scrollable canvas
        self.canvas = tk.Canvas(self.root, bg=self.colors['bg_dark'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        # Configure canvas scrolling
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Main container frame that will be placed inside canvas
        main_frame = ttk.Frame(self.canvas, style='Dark.TFrame', padding="15")
        
        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title with modern design
        title_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 25), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(title_frame, text="⚔️ WoW Bot Pro", style='Title.TLabel')
        title_label.grid(row=0, column=0)
        
        subtitle_label = ttk.Label(title_frame, text="Multiple Windows Automation", 
                                 font=('Segoe UI', 12), 
                                 foreground=self.colors['text_secondary'],
                                 background=self.colors['bg_dark'])
        subtitle_label.grid(row=1, column=0, pady=(5, 0))
        
        # Status section
        self.create_status_section(main_frame)
        
        # Configuration section
        self.create_config_section(main_frame)
        
        # Control section
        self.create_control_section(main_frame)
        
        # Log section
        self.create_log_section(main_frame)
        
        # Bottom info
        self.create_info_section(main_frame)
        
        # Pack scrollbar and canvas with proper weights
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window inside canvas for main_frame
        self.canvas_window = self.canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        # Configure canvas scrolling
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        main_frame.bind('<Configure>', self.on_frame_configure)
        
        # Bind mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind_all("<Button-4>", self.on_mousewheel)
        self.canvas.bind_all("<Button-5>", self.on_mousewheel)
        
        # Bind keyboard scrolling
        self.canvas.bind_all("<Up>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Down>", lambda e: self.canvas.yview_scroll(1, "units"))
        self.canvas.bind_all("<Page_Up>", lambda e: self.canvas.yview_scroll(-10, "units"))
        self.canvas.bind_all("<Page_Down>", lambda e: self.canvas.yview_scroll(10, "units"))
        self.canvas.bind_all("<Home>", lambda e: self.canvas.yview_moveto(0))
        self.canvas.bind_all("<End>", lambda e: self.canvas.yview_moveto(1))
    
    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        # Update canvas window width to match canvas width
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def on_frame_configure(self, event):
        """Handle frame resize and update scroll region"""
        # Update scroll region to encompass all child widgets
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        try:
            if event.num == 4:  # Linux scroll up
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # Linux scroll down
                self.canvas.yview_scroll(1, "units")
            else:  # Windows scroll
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except:
            # Fallback for different mouse wheel implementations
            try:
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except:
                pass
    
    def create_status_section(self, parent):
        """Create modern status display section"""
        status_frame = ttk.LabelFrame(parent, text="📊 System Status", 
                                    style='Dark.TLabelframe', padding="15")
        status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Top row - Main status
        status_top_frame = ttk.Frame(status_frame, style='Medium.TFrame')
        status_top_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Bot status with icon
        self.status_label = ttk.Label(status_top_frame, text="🤖 Bot Status: Stopped", style='Status.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 30))
        
        # Windows info
        self.windows_label = ttk.Label(status_top_frame, text="🪟 Windows: 0 detected", style='Status.TLabel')
        self.windows_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        # Selected windows
        self.selected_label = ttk.Label(status_top_frame, text="✅ Selected: 0", style='Status.TLabel')
        self.selected_label.grid(row=0, column=2, sticky=tk.W)
        
        # Bottom row - Current activity
        status_bottom_frame = ttk.Frame(status_frame, style='Medium.TFrame')
        status_bottom_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Current window
        self.current_window_label = ttk.Label(status_bottom_frame, text="🎯 Current: None", style='Status.TLabel')
        self.current_window_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 30))
        
        # Next action
        self.next_action_label = ttk.Label(status_bottom_frame, text="⏱️ Next action: Not scheduled", style='Status.TLabel')
        self.next_action_label.grid(row=0, column=1, sticky=tk.W)
    
    def create_config_section(self, parent):
        """Create modern configuration section"""
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configuration", 
                                    style='Dark.TLabelframe', padding="15")
        config_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Windows configuration
        windows_frame = ttk.Frame(config_frame, style='Medium.TFrame', padding="10")
        windows_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(windows_frame, text="🪟 WoW Windows Detection", style='Header.TLabel').grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Instructions label
        ttk.Label(windows_frame, text="💡 Click on windows to select/deselect them", 
                 font=('Segoe UI', 9), 
                 foreground=self.colors['text_muted'],
                 background=self.colors['bg_medium']).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # Create two columns for selected and unselected windows
        windows_columns_frame = ttk.Frame(windows_frame, style='Medium.TFrame')
        windows_columns_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Left column - Available Windows (Not Selected)
        available_frame = ttk.LabelFrame(windows_columns_frame, text="📋 Available Windows", 
                                       style='Dark.TLabelframe', padding="10")
        available_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.available_listbox = tk.Listbox(available_frame, height=4, width=35,
                                           bg=self.colors['bg_light'],
                                           fg=self.colors['text_primary'],
                                           selectbackground=self.colors['accent_blue'],
                                           selectforeground=self.colors['text_primary'],
                                           font=('Segoe UI', 9),
                                           relief='flat',
                                           bd=0,
                                           highlightthickness=1,
                                           highlightcolor=self.colors['accent_blue'],
                                           highlightbackground=self.colors['border'],
                                           selectmode=tk.SINGLE)
        self.available_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Bind click event for available windows
        self.available_listbox.bind('<Button-1>', self.on_available_window_click)
        
        # Right column - Selected Windows
        selected_frame = ttk.LabelFrame(windows_columns_frame, text="✅ Selected Windows", 
                                      style='Dark.TLabelframe', padding="10")
        selected_frame.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        self.selected_listbox = tk.Listbox(selected_frame, height=4, width=35,
                                         bg=self.colors['accent_green'],
                                         fg=self.colors['text_primary'],
                                         selectbackground=self.colors['accent_blue'],
                                         selectforeground=self.colors['text_primary'],
                                         font=('Segoe UI', 9),
                                         relief='flat',
                                         bd=0,
                                         highlightthickness=1,
                                         highlightcolor=self.colors['accent_blue'],
                                         highlightbackground=self.colors['border'],
                                         selectmode=tk.SINGLE)
        self.selected_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Bind click event for selected windows
        self.selected_listbox.bind('<Button-1>', self.on_selected_window_click)
        
        # Configure column weights for responsive layout
        windows_columns_frame.columnconfigure(0, weight=1)
        windows_columns_frame.columnconfigure(1, weight=1)
        
        # Modern button frame
        windows_buttons_frame = ttk.Frame(windows_frame, style='Medium.TFrame')
        windows_buttons_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        
        ttk.Button(windows_buttons_frame, text="🔍 Detect Windows", 
                  command=self.detect_windows, style='Config.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(windows_buttons_frame, text="✅ Select All", 
                  command=self.select_all_windows, style='Config.TButton').grid(row=0, column=1, padx=(0, 10))
        ttk.Button(windows_buttons_frame, text="🎯 Select Specific", 
                  command=self.select_specific_windows, style='Config.TButton').grid(row=0, column=2, padx=(0, 10))
        ttk.Button(windows_buttons_frame, text="🗑️ Clear Selection", 
                  command=self.clear_selection, style='Config.TButton').grid(row=0, column=3, padx=(0, 10))
        ttk.Button(windows_buttons_frame, text="🔄 Refresh List", 
                  command=self.refresh_windows_list, style='Config.TButton').grid(row=0, column=4)
        
        # Interval configuration
        interval_frame = ttk.Frame(config_frame, style='Medium.TFrame', padding="10")
        interval_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(interval_frame, text="⏱️ Base Interval (seconds):", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.base_interval_var = tk.StringVar(value=str(self.base_interval))
        self.base_interval_entry = tk.Entry(interval_frame, textvariable=self.base_interval_var, width=12,
                                          bg=self.colors['bg_light'],
                                          fg=self.colors['text_primary'],
                                          font=('Segoe UI', 10),
                                          relief='flat',
                                          bd=0,
                                          insertbackground=self.colors['accent_blue'])
        self.base_interval_entry.grid(row=0, column=1, padx=(15, 0))
        
        ttk.Label(interval_frame, text="🎲 Random Range (seconds):", style='Header.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(30, 0))
        self.random_range_var = tk.StringVar(value=str(self.random_range))
        self.random_range_entry = tk.Entry(interval_frame, textvariable=self.random_range_var, width=12,
                                         bg=self.colors['bg_light'],
                                         fg=self.colors['text_primary'],
                                         font=('Segoe UI', 10),
                                         relief='flat',
                                         bd=0,
                                         insertbackground=self.colors['accent_blue'])
        self.random_range_entry.grid(row=0, column=3, padx=(15, 0))
        
        ttk.Button(interval_frame, text="💾 Apply Settings", 
                  command=self.apply_intervals, style='Config.TButton').grid(row=0, column=4, padx=(30, 0))
    
    def create_control_section(self, parent):
        """Create modern control section"""
        control_frame = ttk.Frame(parent, style='Dark.TFrame', padding="15")
        control_frame.grid(row=3, column=0, columnspan=3, pady=(0, 15))
        
        # Control buttons with modern design
        control_buttons_frame = ttk.Frame(control_frame, style='Dark.TFrame')
        control_buttons_frame.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        self.start_button = ttk.Button(control_buttons_frame, text="🚀 Start Bot", 
                                      command=self.start_bot, style='Start.TButton')
        self.start_button.grid(row=0, column=0, padx=(0, 15))
        
        self.stop_button = ttk.Button(control_buttons_frame, text="⏹️ Stop Bot", 
                                     command=self.stop_bot, style='Stop.TButton', state='disabled')
        self.stop_button.grid(row=0, column=1, padx=(0, 15))
        
        ttk.Button(control_buttons_frame, text="🚨 Emergency Stop (ESC)", 
                  command=self.emergency_stop, style='Emergency.TButton').grid(row=0, column=2)
        
        # Modern progress bar
        progress_frame = ttk.Frame(control_frame, style='Dark.TFrame')
        progress_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        ttk.Label(progress_frame, text="⏳ Progress:", 
                 font=('Segoe UI', 10), 
                 foreground=self.colors['text_secondary'],
                 background=self.colors['bg_dark']).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400, style='Dark.Horizontal.TProgressbar')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Progress percentage label
        self.progress_label = ttk.Label(progress_frame, text="0%", 
                                      font=('Segoe UI', 9), 
                                      foreground=self.colors['text_muted'],
                                      background=self.colors['bg_dark'])
        self.progress_label.grid(row=2, column=0, sticky=tk.W)
        
        control_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(0, weight=1)
    
    def create_log_section(self, parent):
        """Create modern log section"""
        log_frame = ttk.LabelFrame(parent, text="📝 Activity Log", 
                                 style='Dark.TLabelframe', padding="15")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Modern log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=90,
                                                bg=self.colors['bg_light'],
                                                fg=self.colors['text_primary'],
                                                font=('Consolas', 9),
                                                relief='flat',
                                                bd=0,
                                                insertbackground=self.colors['accent_blue'],
                                                selectbackground=self.colors['accent_blue'],
                                                selectforeground=self.colors['text_primary'])
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Modern log controls
        log_controls_frame = ttk.Frame(log_frame, style='Medium.TFrame')
        log_controls_frame.grid(row=1, column=0, sticky=tk.W)
        
        ttk.Button(log_controls_frame, text="🧹 Clear Log", 
                  command=self.clear_log, style='Config.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(log_controls_frame, text="💾 Save Log", 
                  command=self.save_log, style='Config.TButton').grid(row=0, column=1)
    
    def create_info_section(self, parent):
        """Create modern information section"""
        info_frame = ttk.Frame(parent, style='Dark.TFrame', padding="15")
        info_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Modern info labels with icons
        ttk.Label(info_frame, text="⌨️ Controls: ESC to stop | 🖱️ Mouse to upper-left corner for emergency stop", 
                 font=('Segoe UI', 9), 
                 foreground=self.colors['text_secondary'],
                 background=self.colors['bg_dark']).grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(info_frame, text="⚠️ Use at your own risk - Educational purposes only", 
                 font=('Segoe UI', 9, 'bold'), 
                 foreground=self.colors['accent_orange'],
                 background=self.colors['bg_dark']).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
    
    def log_message(self, message, level="INFO"):
        """Add message to log with timestamp and modern styling"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        level_icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "ERROR": "❌",
            "WARNING": "⚠️"
        }
        
        level_colors = {
            "INFO": self.colors['text_primary'],
            "SUCCESS": self.colors['accent_green'],
            "ERROR": self.colors['accent_red'],
            "WARNING": self.colors['accent_orange']
        }
        
        icon = level_icons.get(level, "ℹ️")
        color = level_colors.get(level, self.colors['text_primary'])
        log_entry = f"[{timestamp}] {icon} {level}: {message}\n"
        
        # Insert message
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Color the last line
        try:
            last_line_start = self.log_text.index("end-2c linestart")
            last_line_end = self.log_text.index("end-1c")
            self.log_text.tag_add(level, last_line_start, last_line_end)
            self.log_text.tag_config(level, foreground=color)
        except:
            pass
    
    def detect_windows(self):
        """Detect WoW windows with modern feedback"""
        self.log_message("🔍 Detecting WoW windows...", "INFO")
        
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if "World of Warcraft" in window_title or "WoW" in window_title:
                    try:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        windows.append({
                            'hwnd': hwnd,
                            'title': window_title,
                            'pid': pid
                        })
                    except:
                        windows.append({
                            'hwnd': hwnd,
                            'title': window_title,
                            'pid': None
                        })
            return True
        
        self.wow_windows = []
        win32gui.EnumWindows(enum_windows_callback, self.wow_windows)
        
        # Update listboxes
        self.update_windows_display()
        
        # Update status
        self.windows_label.config(text=f"🪟 Windows: {len(self.wow_windows)} detected")
        self.log_message(f"🎯 Found {len(self.wow_windows)} WoW windows", "SUCCESS")
        
        # Clear previous selection when detecting new windows
        self.selected_windows = []
        self.selected_label.config(text="✅ Selected: 0")
        self.log_message("🔄 Window list refreshed - previous selection cleared", "INFO")
    
    def update_windows_display(self):
        """Update both available and selected windows listboxes"""
        # Clear both listboxes
        self.available_listbox.delete(0, tk.END)
        self.selected_listbox.delete(0, tk.END)
        
        # Populate available windows (not selected)
        for i, window in enumerate(self.wow_windows):
            if window not in self.selected_windows:
                self.available_listbox.insert(tk.END, f"{i+1}. {window['title']}")
        
        # Populate selected windows
        for i, window in enumerate(self.wow_windows):
            if window in self.selected_windows:
                self.selected_listbox.insert(tk.END, f"{i+1}. {window['title']}")
    
    def select_all_windows(self):
        """Select all detected windows"""
        if not self.wow_windows:
            messagebox.showwarning("⚠️ Warning", "No windows detected. Please detect windows first.")
            return
        
        self.selected_windows = self.wow_windows.copy()
        self.selected_label.config(text=f"✅ Selected: {len(self.selected_windows)}")
        
        # Update display
        self.update_windows_display()
        
        self.log_message(f"✅ Selected all {len(self.selected_windows)} windows", "SUCCESS")
    
    def clear_selection(self):
        """Clear window selection"""
        self.selected_windows = []
        self.selected_label.config(text="✅ Selected: 0")
        
        # Update display
        self.update_windows_display()
        
        self.log_message("🗑️ Cleared window selection", "INFO")
    
    def select_specific_windows(self):
        """Select specific windows by number input"""
        if not self.wow_windows:
            messagebox.showwarning("⚠️ Warning", "No windows detected. Please detect windows first.")
            return
        
        # Create a simple dialog for number input
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Specific Windows")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Instructions
        tk.Label(dialog, text="Enter window numbers to select (e.g., 1,3,5)", 
                font=('Segoe UI', 12, 'bold'),
                fg=self.colors['text_primary'],
                bg=self.colors['bg_dark']).pack(pady=20)
        
        # Available windows list
        tk.Label(dialog, text="Available Windows:", 
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['accent_blue'],
                bg=self.colors['bg_dark']).pack(pady=(0, 10))
        
        windows_text = tk.Text(dialog, height=8, width=50,
                              bg=self.colors['bg_light'],
                              fg=self.colors['text_primary'],
                              font=('Segoe UI', 9),
                              relief='flat',
                              bd=0)
        windows_text.pack(pady=(0, 20))
        
        for i, window in enumerate(self.wow_windows):
            windows_text.insert(tk.END, f"{i+1}. {window['title']}\n")
        windows_text.config(state=tk.DISABLED)
        
        # Input field
        tk.Label(dialog, text="Window numbers (comma separated):", 
                font=('Segoe UI', 10),
                fg=self.colors['text_secondary'],
                bg=self.colors['bg_dark']).pack(pady=(0, 5))
        
        entry = tk.Entry(dialog, width=30,
                        bg=self.colors['bg_light'],
                        fg=self.colors['text_primary'],
                        font=('Segoe UI', 10),
                        relief='flat',
                        bd=0,
                        insertbackground=self.colors['accent_blue'])
        entry.pack(pady=(0, 20))
        entry.focus()
        
        def apply_selection():
            try:
                numbers_text = entry.get().strip()
                if not numbers_text:
                    messagebox.showwarning("⚠️ Warning", "Please enter window numbers!")
                    return
                
                # Parse numbers
                numbers = [int(x.strip()) for x in numbers_text.split(',')]
                
                # Validate numbers
                if not all(1 <= n <= len(self.wow_windows) for n in numbers):
                    messagebox.showerror("❌ Error", f"Please enter numbers between 1 and {len(self.wow_windows)}")
                    return
                
                # Clear current selection
                self.clear_selection()
                
                # Select specified windows
                for num in numbers:
                    window_index = num - 1
                    window_info = self.wow_windows[window_index]
                    self.selected_windows.append(window_info)
                
                self.selected_label.config(text=f"✅ Selected: {len(self.selected_windows)}")
                self.log_message(f"✅ Selected specific windows: {', '.join(map(str, numbers))}", "SUCCESS")
                
                # Update display
                self.update_windows_display()
                
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("❌ Error", "Please enter valid numbers separated by commas!")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="✅ Apply", 
                 command=apply_selection,
                 bg=self.colors['accent_green'],
                 fg=self.colors['text_primary'],
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat',
                 bd=0,
                 padx=20,
                 pady=5).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="❌ Cancel", 
                 command=dialog.destroy,
                 bg=self.colors['accent_red'],
                 fg=self.colors['text_primary'],
                 font=('Segoe UI', 10, 'bold'),
                 relief='flat',
                 bd=0,
                 padx=20,
                 pady=5).pack(side=tk.LEFT)
        
        # Bind Enter key
        entry.bind('<Return>', lambda e: apply_selection())
        entry.bind('<Escape>', lambda e: dialog.destroy())
    
    def apply_intervals(self):
        """Apply new interval settings"""
        try:
            new_base = float(self.base_interval_var.get())
            new_range = float(self.random_range_var.get())
            
            if new_base <= 0 or new_range < 0:
                messagebox.showerror("❌ Error", "Intervals must be positive numbers")
                return
            
            self.base_interval = new_base
            self.random_range = new_range
            
            self.log_message(f"💾 Intervals updated: Base={new_base}s, Range={new_range}s", "SUCCESS")
            messagebox.showinfo("✅ Success", f"Intervals updated!\nBase: {new_base}s\nRange: 0-{new_range}s")
            
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter valid numbers")
    
    def start_bot(self):
        """Start the bot with modern UI updates"""
        if not self.selected_windows:
            messagebox.showwarning("⚠️ Warning", "Please select windows first!")
            return
        
        if self.bot_running:
            return
        
        self.bot_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_label.config(text="🤖 Bot Status: Running", foreground=self.colors['accent_green'])
        
        # Start bot in separate thread
        self.bot_thread = threading.Thread(target=self.bot_worker, daemon=True)
        self.bot_thread.start()
        
        self.log_message("🚀 Bot started!", "SUCCESS")
    
    def stop_bot(self):
        """Stop the bot with modern UI updates"""
        self.bot_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="🤖 Bot Status: Stopped", foreground=self.colors['accent_red'])
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self.next_action_label.config(text="⏱️ Next action: Not scheduled")
        self.current_window_label.config(text="🎯 Current: None")
        
        self.log_message("⏹️ Bot stopped!", "WARNING")
    
    def emergency_stop(self):
        """Emergency stop the bot"""
        self.stop_bot()
        self.log_message("🚨 EMERGENCY STOP ACTIVATED!", "ERROR")
    
    def bot_worker(self):
        """Main bot worker function"""
        try:
            while self.bot_running:
                if not self.selected_windows:
                    break
                
                # Switch to next window
                current_window = self.selected_windows[self.current_window_index]
                self.current_window_label.config(text=f"🎯 Current: {current_window['title'][:30]}...")
                
                if self.switch_to_window(current_window):
                    # Press and hold '0' for a random duration (0.1–1.0s)
                    hold_duration = random.uniform(0.1, 1.0)
                    pyautogui.keyDown('0')
                    time.sleep(hold_duration)
                    pyautogui.keyUp('0')
                    current_time = time.strftime('%H:%M:%S')
                    self.log_message(f"⌨️ Key '0' pressed (held {hold_duration:.2f}s) in window '{current_window['title']}' at {current_time}", "SUCCESS")
                    
                    # Move to next window
                    self.current_window_index = (self.current_window_index + 1) % len(self.selected_windows)
                else:
                    self.log_message(f"❌ Error switching to window: {current_window['title']}", "ERROR")
                
                # Calculate next interval
                next_interval = self.get_random_interval()
                self.next_action_label.config(text=f"⏱️ Next action: {next_interval:.1f}s")
                
                # Progress bar animation
                self.animate_progress(next_interval)
                
                # Wait for interval
                time.sleep(next_interval)
                
        except Exception as e:
            self.log_message(f"❌ Bot error: {e}", "ERROR")
            self.stop_bot()
    
    def switch_to_window(self, window):
        """Switch to a specific window"""
        try:
            if win32gui.IsIconic(window['hwnd']):
                win32gui.ShowWindow(window['hwnd'], win32con.SW_RESTORE)
            
            win32gui.SetForegroundWindow(window['hwnd'])
            time.sleep(0.5)
            return True
        except Exception as e:
            return False
    
    def get_random_interval(self):
        """Get random interval"""
        random_addition = random.uniform(0, self.random_range)
        return self.base_interval + random_addition
    
    def animate_progress(self, duration):
        """Animate progress bar with percentage updates"""
        steps = 100
        step_time = duration / steps
        
        for i in range(steps):
            if not self.bot_running:
                break
            progress = i + 1
            self.progress_var.set(progress)
            self.progress_label.config(text=f"{progress}%")
            time.sleep(step_time)
    
    def clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("🧹 Log cleared", "INFO")
    
    def save_log(self):
        """Save log to file"""
        try:
            filename = f"wow_bot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.log_text.get(1.0, tk.END))
            self.log_message(f"💾 Log saved to {filename}", "SUCCESS")
        except Exception as e:
            self.log_message(f"❌ Error saving log: {e}", "ERROR")

    def on_available_window_click(self, event):
        """Handle click on the 'Available Windows' listbox to select windows"""
        widget = event.widget
        selection = widget.curselection()
        
        if selection:
            index = selection[0]
            # Find the actual window in wow_windows list
            available_windows = [w for w in self.wow_windows if w not in self.selected_windows]
            if 0 <= index < len(available_windows):
                window_info = available_windows[index]
                
                # Add to selected windows
                self.selected_windows.append(window_info)
                self.selected_label.config(text=f"✅ Selected: {len(self.selected_windows)}")
                self.log_message(f"✅ Selected window: {window_info['title']}", "SUCCESS")
                
                # Update display
                self.update_windows_display()
    
    def on_selected_window_click(self, event):
        """Handle click on the 'Selected Windows' listbox to deselect windows"""
        widget = event.widget
        selection = widget.curselection()
        
        if selection:
            index = selection[0]
            # Find the actual window in selected_windows list
            if 0 <= index < len(self.selected_windows):
                window_info = self.selected_windows[index]
                
                # Remove from selected windows
                self.selected_windows.remove(window_info)
                self.selected_label.config(text=f"✅ Selected: {len(self.selected_windows)}")
                self.log_message(f"❌ Deselected window: {window_info['title']}", "INFO")
                
                # Update display
                self.update_windows_display()

    def refresh_windows_list(self):
        """Refresh the list of detected windows"""
        self.detect_windows()

def main():
    # pyautogui safety settings
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    root = tk.Tk()
    app = WoWBotGUI(root)
    
    # Handle window close
    def on_closing():
        if app.bot_running:
            if messagebox.askokcancel("⚠️ Quit", "Bot is running. Stop it and quit?"):
                app.stop_bot()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start GUI
    root.mainloop()

if __name__ == "__main__":
    main()
