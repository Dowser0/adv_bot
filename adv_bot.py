import pyautogui
import time
import keyboard
import sys
import random
import win32gui
import win32con
import win32process

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
        """Switches to a specific window"""
        try:
            # Restore window if minimized
            if win32gui.IsIconic(window['hwnd']):
                win32gui.ShowWindow(window['hwnd'], win32con.SW_RESTORE)
            
            # Bring window to front
            win32gui.SetForegroundWindow(window['hwnd'])
            
            # Wait a bit for window to gain focus
            time.sleep(0.5)
            
            return True
        except Exception as e:
            print(f"Error switching to window: {e}")
            return False
    
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
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        
        self.running = True
        print("Bot started! Switching between windows and pressing '0'...")
        
        try:
            while self.running:
                # Check if ESC was pressed
                if keyboard.is_pressed('esc'):
                    print("ESC pressed! Stopping bot...")
                    break
                
                # Switch to next window
                current_window = self.selected_windows[self.current_window_index]
                if self.switch_to_window(current_window):
                    # Press the '0' key
                    pyautogui.press('0')
                    current_time = time.strftime('%H:%M:%S')
                    print(f"Key '0' pressed in window '{current_window['title']}' at {current_time}")
                    
                    # Move to next window
                    self.current_window_index = (self.current_window_index + 1) % len(self.selected_windows)
                else:
                    print(f"Error switching to window: {current_window['title']}")
                
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
    
    def configure_windows(self):
        """Configures WoW windows"""
        print("Looking for World of Warcraft windows...")
        self.find_wow_windows()
        
        if not self.wow_windows:
            print("No WoW windows found!")
            print("Make sure World of Warcraft is running.")
            return False
        
        return self.select_windows()

def main():
    bot = WoWBot()
    
    print("=== MULTIPLE WINDOWS WOW BOT ===")
    print("1. Configure WoW windows")
    print("2. Start bot")
    print("3. Change base interval")
    print("4. Change random range")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nChoose an option (1-5): ").strip()
            
            if choice == '1':
                if bot.configure_windows():
                    print("Window configuration completed!")
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
                    else:
                        print("Interval must be greater than 0!")
                except ValueError:
                    print("Please enter a valid number!")
            elif choice == '4':
                try:
                    new_range = float(input("Enter new random range in seconds: "))
                    if new_range >= 0:
                        bot.set_random_range(new_range)
                    else:
                        print("Range must be greater than or equal to 0!")
                except ValueError:
                    print("Please enter a valid number!")
            elif choice == '5':
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid option! Choose 1, 2, 3, 4 or 5.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    main() 