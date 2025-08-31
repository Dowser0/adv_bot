import pyautogui
import time
import keyboard
import sys
import random
import win32gui
import win32con
import win32process
import win32api
import json
import os

class WoWBot:
    def __init__(self):
        # pyautogui safety settings
        pyautogui.FAILSAFE = True  # Move mouse to upper left corner to stop
        pyautogui.PAUSE = 0.1  # Small pause between actions
        
        self.running = False
        self.base_interval = 2.0  # Base interval in seconds
        self.random_range = 10.0  # Additional random range in seconds
        self.wow_windows = []  # List of WoW windows
        self.selected_windows = []  # Windows selected for the bot
        self.current_window_index = 0  # Current window index
        
        # Configuration file path
        self.config_file = "wow_bot_config.json"
        
        # Load saved configuration on startup
        self.load_configuration()
        
    def find_wow_windows(self):
        """Finds all World of Warcraft windows"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if "World of Warcraft" in window_title or "WoW" in window_title:
                    try:
                        # Try to get process PID
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
        return self.wow_windows
    
    def select_windows(self):
        """Allows user to select which windows to use"""
        if not self.wow_windows:
            print("No WoW windows found!")
            return False
        
        print(f"\n=== WOW WINDOWS FOUND ({len(self.wow_windows)}) ===")
        for i, window in enumerate(self.wow_windows):
            print(f"{i+1}. {window['title']}")
        
        print("\nOptions:")
        print("1. Select specific windows")
        print("2. Use all windows")
        print("3. Cancel")
        
        while True:
            try:
                choice = input("\nChoose an option (1-3): ").strip()
                
                if choice == '1':
                    return self.select_specific_windows()
                elif choice == '2':
                    self.selected_windows = self.wow_windows.copy()
                    print(f"All {len(self.selected_windows)} windows selected!")
                    return True
                elif choice == '3':
                    return False
                else:
                    print("Invalid option! Choose 1, 2 or 3.")
            except KeyboardInterrupt:
                return False
    
    def select_specific_windows(self):
        """Allows selecting specific windows"""
        print("\nEnter the numbers of the windows you want to use (separated by comma):")
        print("Example: 1,3,5")
        
        try:
            selection = input("Selection: ").strip()
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            
            # Validate indices
            valid_indices = [i for i in indices if 0 <= i < len(self.wow_windows)]
            if not valid_indices:
                print("No valid indices selected!")
                return False
            
            self.selected_windows = [self.wow_windows[i] for i in valid_indices]
            print(f"{len(self.selected_windows)} windows selected!")
            return True
            
        except (ValueError, KeyboardInterrupt):
            print("Invalid selection!")
            return False
    
    def switch_to_window(self, window):
        """Prepares window for input without bringing it to focus"""
        try:
            # Restore window if minimized (but don't bring to front)
            if win32gui.IsIconic(window['hwnd']):
                win32gui.ShowWindow(window['hwnd'], win32con.SW_RESTORE)
            
            # Don't use SetForegroundWindow - this prevents focus stealing
            # win32gui.SetForegroundWindow(window['hwnd'])
            
            # Small delay to ensure window is ready
            time.sleep(0.1)
            
            return True
        except Exception as e:
            print(f"Error preparing window: {e}")
            return False
    
    def send_key_to_window(self, window, key):
        """Sends a key press directly to a specific window without focusing it"""
        try:
            hwnd = window['hwnd']
            
            # Virtual key codes
            vk_0 = 0x30      # Virtual key code for '0'
            vk_a = 0x41      # Virtual key code for 'A'
            vk_d = 0x44      # Virtual key code for 'D'
            vk_s = 0x53      # Virtual key code for 'S'
            vk_w = 0x57      # Virtual key code for 'W'
            
            # Random duration for '0' key (0.1-1.0 seconds)
            hold_duration_0 = random.uniform(0.1, 1.0)
            
            # Send '0' key with random hold duration
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_0, 0)
            time.sleep(hold_duration_0)
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_0, 0)
            
            # Small delay between actions
            time.sleep(0.1)
            
            # Random duration for anti-AFK movement (0.1-0.5 seconds)
            hold_duration_movement = random.uniform(0.1, 0.5)
            
            # Random anti-AFK movement (A, D, S, or W)
            movement_options = [
                (vk_a, 'A'),  # Left
                (vk_d, 'D'),  # Right
                (vk_s, 'S'),  # Down
                (vk_w, 'W')   # Up
            ]
            
            # Pick random movement
            chosen_movement = random.choice(movement_options)
            vk_movement, movement_key = chosen_movement
            
            # Send anti-AFK movement key
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_movement, 0)
            time.sleep(hold_duration_movement)
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_movement, 0)
            
            return True, movement_key, hold_duration_0, hold_duration_movement
        except Exception as e:
            print(f"Error sending key to window: {e}")
            return False, None, None, None
    
    def get_random_interval(self):
        """Returns a random interval between base_interval and base_interval + random_range"""
        random_addition = random.uniform(0, self.random_range)
        total_interval = self.base_interval + random_addition
        return total_interval
        
    def start_bot(self):
        """Starts the bot that presses '0' with random intervals in multiple WoW windows"""
        if not self.selected_windows:
            print("No windows selected! Use the configuration option first.")
            return
        
        print("=== WORLD OF WARCRAFT BOT - MULTIPLE WINDOWS ===")
        print(f"Using {len(self.selected_windows)} WoW windows")
        print(f"Presses '0' every {self.base_interval}-{self.base_interval + self.random_range} seconds (random)")
        print("Press 'ESC' to stop the bot")
        print("Move mouse to upper left corner for emergency stop")
        print("Bot starting in 3 seconds...")
        print("Note: Windows will NOT be brought to focus - keys sent directly!")
        print("Anti-AFK: Character will move left/right to prevent disconnection!")
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        
        self.running = True
        print("Bot started! Sending '0' key + anti-AFK movement to windows...")
        
        try:
            while self.running:
                # Check if ESC was pressed
                if keyboard.is_pressed('esc'):
                    print("ESC pressed! Stopping bot...")
                    break
                
                # Prepare next window (without focusing)
                current_window = self.selected_windows[self.current_window_index]
                if self.switch_to_window(current_window):
                    # Send the '0' key and anti-AFK movement directly to the window
                    result = self.send_key_to_window(current_window, '0')
                    if result[0]:  # Success
                        movement = result[1]
                        hold_0 = result[2]
                        hold_movement = result[3]
                        current_time = time.strftime('%H:%M:%S')
                        print(f"Key '0' (held {hold_0:.2f}s) + movement '{movement}' (held {hold_movement:.2f}s) sent to window '{current_window['title']}' at {current_time}")
                    else:
                        print(f"Error sending keys to window: {current_window['title']}")
                    
                    # Move to next window
                    self.current_window_index = (self.current_window_index + 1) % len(self.selected_windows)
                else:
                    print(f"Error preparing window: {current_window['title']}")
                
                # Calculate and display next interval
                next_interval = self.get_random_interval()
                print(f"Next action in {next_interval:.1f} seconds")
                
                # Wait for random interval
                time.sleep(next_interval)
                
        except KeyboardInterrupt:
            print("\nBot interrupted by user!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.stop_bot()
    
    def stop_bot(self):
        """Stops the bot"""
        self.running = False
        print("Bot stopped!")
    
    def set_base_interval(self, seconds):
        """Sets the base interval between key presses"""
        self.base_interval = seconds
        print(f"Base interval changed to {seconds} seconds")
        print(f"Total interval will be between {seconds}-{seconds + self.random_range} seconds")
    
    def set_random_range(self, seconds):
        """Sets the additional random range"""
        self.random_range = seconds
        print(f"Random range changed to {seconds} seconds")
        print(f"Total interval will be between {self.base_interval}-{self.base_interval + seconds} seconds")
    
    def save_configuration(self):
        """Saves current configuration to file"""
        try:
            config = {
                'base_interval': self.base_interval,
                'random_range': self.random_range
                # Removed selected_windows from saved configuration
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False
    
    def load_configuration(self):
        """Loads configuration from file"""
        try:
            if not os.path.exists(self.config_file):
                print("📁 No configuration file found. Starting with default settings.")
                return False
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Load basic settings only
            if 'base_interval' in config:
                self.base_interval = config['base_interval']
            if 'random_range' in config:
                self.random_range = config['random_range']
            
            print(f"✅ Configuration loaded from {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            return False
    
    def configure_windows(self):
        """Configures WoW windows"""
        print("Looking for World of Warcraft windows...")
        self.find_wow_windows()
        
        if not self.wow_windows:
            print("No WoW windows found!")
            print("Make sure World of Warcraft is running.")
            return False
        
        # Always go to window selection (no auto-validation of saved windows)
        return self.select_windows()

def main():
    bot = WoWBot()
    
    print("=== MULTIPLE WINDOWS WOW BOT ===")
    print("1. Configure WoW windows")
    print("2. Start bot")
    print("3. Change base interval")
    print("4. Change random range")
    print("5. Save current configuration")
    print("6. Load configuration")
    print("7. Exit")
    
    while True:
        try:
            choice = input("\nChoose an option (1-7): ").strip()
            
            if choice == '1':
                if bot.configure_windows():
                    print("Window configuration completed!")
                    # No auto-save after window configuration
                else:
                    print("Configuration cancelled!")
            elif choice == '2':
                if bot.selected_windows:
                    bot.start_bot()
                    break
                else:
                    print("Configure windows first (option 1)!")
            elif choice == '3':
                try:
                    new_interval = float(input("Enter new base interval in seconds: "))
                    if new_interval > 0:
                        bot.set_base_interval(new_interval)
                        # Auto-save after changing settings
                        bot.save_configuration()
                    else:
                        print("Interval must be greater than 0!")
                except ValueError:
                    print("Please enter a valid number!")
            elif choice == '4':
                try:
                    new_range = float(input("Enter new random range in seconds: "))
                    if new_range >= 0:
                        bot.set_random_range(new_range)
                        # Auto-save after changing settings
                        bot.save_configuration()
                    else:
                        print("Range must be greater than or equal to 0!")
                except ValueError:
                    print("Please enter a valid number!")
            elif choice == '5':
                if bot.save_configuration():
                    print("Configuration saved successfully!")
                else:
                    print("Failed to save configuration!")
            elif choice == '6':
                if bot.load_configuration():
                    print("Configuration loaded successfully!")
                else:
                    print("Failed to load configuration!")
            elif choice == '7':
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid option! Choose 1, 2, 3, 4, 5, 6 or 7.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    main() 