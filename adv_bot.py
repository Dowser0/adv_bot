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
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.columns import Columns
from rich.rule import Rule

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
        self.dry_run = False  # When True, simulates actions without sending keys
        self.console = Console()
        self.anti_afk_enabled = True  # Controls anti-AFK movement
        self.stop_hotkey = None  # Handle for global stop hotkey
        # Configuration file path and initial load
        self.config_file = "wow_bot_config.json"
        try:
            self.load_configuration()
        except Exception:
            pass

    def render_header(self):
        title = Text("WOW BOT", justify="center", style="bold white")
        subtitle = Text("Advertisement", justify="center", style="dim")
        header_panel = Panel.fit(title, subtitle=subtitle, border_style="cyan")
        self.console.print(header_panel)
        self.console.print(Rule(style="grey50"))

    def render_quick_status(self):
        """Renders a compact status bar with key metrics above the menu."""
        selected_count = len(self.selected_windows)
        anti_afk_state = "on" if self.anti_afk_enabled else "off"
        anti_afk_color = "green" if self.anti_afk_enabled else "red"
        panels = [
            Panel(f"{selected_count}", title="Selected", border_style="cyan"),
            Panel(f"{self.base_interval:.1f}s", title="Base interval", border_style="cyan"),
            Panel(f"{self.random_range:.1f}s", title="Random range", border_style="cyan"),
            Panel(Text(anti_afk_state, style=f"bold {anti_afk_color}"), title="Anti-AFK", border_style=anti_afk_color),
        ]
        self.console.print(Columns(panels, equal=True, expand=True))
        self.console.print(Rule(style="grey50"))
        
        
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
        """Allows user to select which windows to use (modern checkbox UI)"""
        if not self.wow_windows:
            self.console.print("[bold red]No WoW windows found![/bold red]")
            return False

        choices = [f"{i+1}. {w['title']}" for i, w in enumerate(self.wow_windows)]
        try:
            picked = questionary.checkbox(
                "Select WoW windows (space to toggle, enter to confirm)",
                choices=choices,
                qmark="",
            ).ask()
            if not picked:
                self.console.print("[yellow]No windows selected.[/yellow]")
                return False
            indices = []
            for label in picked:
                try:
                    idx = int(label.split(".")[0]) - 1
                    indices.append(idx)
                except Exception:
                    continue
            valid_indices = [i for i in indices if 0 <= i < len(self.wow_windows)]
            if not valid_indices:
                self.console.print("[yellow]Invalid selection.[/yellow]")
                return False
            self.selected_windows = [self.wow_windows[i] for i in valid_indices]
            self.console.print(f"[green]{len(self.selected_windows)} window(s) selected![/green]")
            return True
        except KeyboardInterrupt:
            return False
    
    def select_specific_windows(self):
        """Legacy input selection kept for fallback; not used in new UI"""
        try:
            return self.select_windows()
        except Exception:
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
            
            # Send '0' key with random hold duration (skip when dry_run)
            if not self.dry_run:
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_0, 0)
                time.sleep(hold_duration_0)
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_0, 0)
            else:
                time.sleep(hold_duration_0)
            
            # Small delay between actions
            time.sleep(0.1)
            
            movement_key = None
            hold_duration_movement = None
            if self.anti_afk_enabled:
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
                
                # Send anti-AFK movement key (skip when dry_run)
                if not self.dry_run:
                    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_movement, 0)
                    time.sleep(hold_duration_movement)
                    win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_movement, 0)
                else:
                    time.sleep(hold_duration_movement)
            
            return True, movement_key, hold_duration_0, hold_duration_movement
        except Exception as e:
            print(f"Error sending key to window: {e}")
            return False, None, None, None
    
    def get_random_interval(self):
        """Returns a random interval between base_interval and base_interval + random_range"""
        random_addition = random.uniform(0, self.random_range)
        total_interval = self.base_interval + random_addition
        return total_interval

    def is_stop_requested(self):
        """Checks if F8 is pressed using Win32 API (works even during sleeps)."""
        try:
            # VK_F8 = 0x77
            state = win32api.GetAsyncKeyState(0x77)
            return (state & 0x8000) != 0
        except Exception:
            try:
                return keyboard.is_pressed('f8')
            except Exception:
                return False

    def wait_with_stop(self, seconds):
        """Wait up to 'seconds' with 100ms polling for F8. Returns True if stopped early."""
        end_time = time.time() + seconds
        while time.time() < end_time and self.running:
            if self.is_stop_requested():
                self.console.print("[yellow]Stopping bot and returning to menu...[/yellow]")
                self.running = False
                return True
            time.sleep(0.1)
        return not self.running
        
    def start_bot(self):
        """Starts the bot that presses '0' with random intervals in multiple WoW windows"""
        if not self.selected_windows:
            print("No windows selected! Use the configuration option first.")
            return
        
        self.console.print(Panel.fit(Text("WORLD OF WARCRAFT BOT", justify="center", style="bold white"), subtitle="Multiple windows", border_style="cyan"))
        self.console.print(f"Using [bold]{len(self.selected_windows)}[/bold] WoW window(s)")
        # Refresh configuration display values just in case
        try:
            self.load_configuration()
        except Exception:
            pass
        self.console.print(f"Pressing '0' every [bold]{self.base_interval}-{self.base_interval + self.random_range}[/bold]s (random)")
        self.console.print("Press [bold]F8[/bold] to stop and return to menu | Mouse upper-left = emergency stop")
        self.console.print("Starting in 3 seconds...")
        self.console.print("[dim]Windows will not be focused; keys sent directly.[/dim]")
        if self.anti_afk_enabled:
            self.console.print("[dim]Anti-AFK: on (small A/D/S/W movement). Press F8 to stop.[/dim]")
        else:
            self.console.print("[dim]Anti-AFK: off. Press F8 to stop.[/dim]")
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"Starting in {i}...")
            time.sleep(1)
        
        self.running = True
        print("Bot started! Sending '0' key + anti-AFK movement to windows...")
        
        try:
            while self.running:
                
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
                        if movement is not None and hold_movement is not None:
                            self.console.print(f"[green]✓[/green] '0' ({hold_0:.2f}s) + move '[bold]{movement}[/bold]' ({hold_movement:.2f}s) on '[cyan]{current_window['title']}[/cyan]' at {current_time}")
                        else:
                            self.console.print(f"[green]✓[/green] '0' ({hold_0:.2f}s) on '[cyan]{current_window['title']}[/cyan]' at {current_time}")
                    else:
                        self.console.print(f"[red]Error sending keys to:[/red] {current_window['title']}")
                    
                    # Move to next window
                    self.current_window_index = (self.current_window_index + 1) % len(self.selected_windows)
                else:
                    self.console.print(f"[red]Error preparing window:[/red] {current_window['title']}")
                
                # Calculate and display next interval
                next_interval = self.get_random_interval()
                self.console.print(f"Next action in [bold]{next_interval:.1f}s[/bold]")
                
                # Wait for random interval with F8 interruption support
                if self.wait_with_stop(next_interval):
                    break
                
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Bot interrompido pelo usuário![/bold yellow]")
        except Exception as e:
            self.console.print(f"[red]Erro:[/red] {e}")
        finally:
            self.stop_bot()

    def test_cycle(self):
        """Performs a single dry-run cycle across selected windows (no keys actually sent)"""
        if not self.selected_windows:
            print("Configure windows first (option 1)!")
            return
        self.console.print(Panel("No keys will be sent. Simulating timings and movements.", title="TEST (DRY-RUN)", border_style="magenta"))
        original_dry_run = self.dry_run
        self.dry_run = True
        try:
            for idx, window in enumerate(self.selected_windows):
                if self.switch_to_window(window):
                    ok, movement, hold_0, hold_move = self.send_key_to_window(window, '0')
                    if ok:
                        self.console.print(f"[{idx+1}/{len(self.selected_windows)}] '0' ({hold_0:.2f}s) + move '{movement}' ({hold_move:.2f}s) on '[cyan]{window['title']}[/cyan]'")
                    else:
                        self.console.print(f"[red]Failed to simulate send to:[/red] {window['title']}")
                else:
                    self.console.print(f"[red]Failed to prepare window:[/red] {window['title']}")
        finally:
            self.dry_run = original_dry_run
        self.console.print("[green]Test completed. No actions were sent.[/green]")

    def show_status(self):
        """Displays a concise status overview"""
        table = Table(title="Status", box=box.SIMPLE_HEAVY)
        table.add_column("Item", style="bold cyan")
        table.add_column("Value", style="white")
        table.add_row("Found windows", str(len(self.wow_windows)))
        if self.selected_windows:
            titles = "\n".join([f"{i+1}. {w['title']}" for i, w in enumerate(self.selected_windows)])
            table.add_row("Selected", titles)
        else:
            table.add_row("Selected", "None")
        table.add_row("Base interval", f"{self.base_interval:.1f}s")
        table.add_row("Random range", f"{self.random_range:.1f}s")
        table.add_row("Total interval", f"{self.base_interval:.1f}-{self.base_interval + self.random_range:.1f}s")
        table.add_row("Test mode", "on" if self.dry_run else "off")
        table.add_row("Anti-AFK", "on" if self.anti_afk_enabled else "off")
        self.console.print(table)
    
    def stop_bot(self):
        """Stops the bot"""
        self.running = False
        self.console.print("[bold]Bot stopped![/bold]")
    
    def set_base_interval(self, seconds):
        """Sets the base interval between key presses"""
        self.base_interval = seconds
        self.console.print(f"Base interval set to [bold]{seconds}[/bold] seconds")
        self.console.print(f"Total between [bold]{seconds}-{seconds + self.random_range}[/bold] seconds")
        # Auto-save whenever value changes
        self.save_configuration()
    
    def set_random_range(self, seconds):
        """Sets the additional random range"""
        self.random_range = seconds
        self.console.print(f"Random range set to [bold]{seconds}[/bold] seconds")
        self.console.print(f"Total between [bold]{self.base_interval}-{self.base_interval + seconds}[/bold] seconds")
        # Auto-save whenever value changes
        self.save_configuration()

    def set_anti_afk_enabled(self, enabled):
        """Enable or disable anti-AFK and persist setting"""
        self.anti_afk_enabled = bool(enabled)
        state = "on" if self.anti_afk_enabled else "off"
        self.console.print(f"Anti-AFK is now [bold]{state}[/bold].")
        # Auto-save toggle
        self.save_configuration()
    
    def save_configuration(self):
        """Saves current configuration to file"""
        try:
            config = {
                'base_interval': self.base_interval,
                'random_range': self.random_range,
                'anti_afk_enabled': self.anti_afk_enabled
                # Removed selected_windows from saved configuration
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.console.print(f"✅ Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            self.console.print(f"❌ Erro ao salvar configuração: {e}")
            return False
    
    def load_configuration(self):
        """Loads configuration from file"""
        try:
            if not os.path.exists(self.config_file):
                return False
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Load basic settings only
            if 'base_interval' in config:
                self.base_interval = config['base_interval']
            if 'random_range' in config:
                self.random_range = config['random_range']
            if 'anti_afk_enabled' in config:
                self.anti_afk_enabled = bool(config['anti_afk_enabled'])
            
            return True
            
        except Exception as e:
            # Silent config errors as requested
            return False
    
    def configure_windows(self):
        """Configures WoW windows"""
        with self.console.status("Searching for World of Warcraft windows...", spinner="dots"):
            self.find_wow_windows()
        
        if not self.wow_windows:
            self.console.print("[red]No WoW windows found![/red]")
            self.console.print("Make sure World of Warcraft is running.")
            return False
        
        # Always go to window selection (no auto-validation of saved windows)
        return self.select_windows()

def main():
    # Limpar tela no início para ocultar qualquer texto anterior do console
    try:
        os.system('cls')
    except Exception:
        pass
    bot = WoWBot()
    bot.render_header()

    def ask_number(prompt_message, allow_zero=False):
        def validate(text):
            try:
                value = float(text)
                if not allow_zero and value <= 0:
                    return "Must be greater than 0"
                if allow_zero and value < 0:
                    return "Cannot be negative"
                return True
            except Exception:
                return "Enter a valid number"
        ans = questionary.text(prompt_message, validate=validate, qmark="").ask()
        return float(ans) if ans is not None else None

    while True:
        try:
            # Clear and render header each loop for a clean look
            bot.console.clear()
            bot.render_header()
            bot.render_quick_status()
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    "Configure WoW windows",
                    "Start bot",
                    "Anti-AFK (on/off)",
                    "Change base interval",
                    "Change random range",
                    "Exit",
                ],
                qmark="",
            ).ask()

            if action == "Configure WoW windows":
                if bot.configure_windows():
                    bot.console.print("[green]Window configuration completed![/green]")
                else:
                    bot.console.print("[yellow]Configuration canceled![/yellow]")
            elif action == "Start bot":
                if bot.selected_windows:
                    bot.start_bot()
                else:
                    bot.console.print("[yellow]Select windows first.[/yellow]")
            elif action == "Anti-AFK (on/off)":
                bot.set_anti_afk_enabled(not bot.anti_afk_enabled)
            elif action == "Change base interval":
                value = ask_number("New base interval (s): ")
                if value is not None:
                    bot.set_base_interval(value)
                    bot.save_configuration()
            elif action == "Change random range":
                value = ask_number("New random range (s): ", allow_zero=True)
                if value is not None:
                    bot.set_random_range(value)
                    bot.save_configuration()
            elif action == "Exit":
                bot.console.print("Exiting...")
                sys.exit(0)
            else:
                bot.console.print("[yellow]Invalid option![/yellow]")

        except KeyboardInterrupt:
            bot.console.print("\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    main() 