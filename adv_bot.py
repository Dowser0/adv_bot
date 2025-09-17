import pyautogui
import time
import keyboard
import sys
import random
import json
import os
from datetime import datetime

import win32gui
import win32con
import win32process
import win32api
import win32ui
import ctypes
from ctypes import wintypes
from PIL import Image
import numpy as np
import cv2
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
from rich.columns import Columns
from rich.rule import Rule

# Constants
VK_CODES = {
    '0': 0x30, 'A': 0x41, 'D': 0x44, 'S': 0x53, 'W': 0x57, 'ENTER': 0x0D, 'F8': 0x77
}
DEFAULT_CONFIG = {
    'base_interval': 2.0,
    'random_range': 10.0,
    'anti_afk_enabled': True,
    'screenshots_enabled': True,
    'element_detection_enabled': True,
    'element1_template_path': "elemento1.png",
    'element2_template_path': "elemento2.png",
    'detection_threshold': 0.7,
    'wait_after_click': 5.0
}

class WoWBot:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        self.running = False
        self.wow_windows = []
        self.selected_windows = []
        self.current_window_index = 0
        self.dry_run = False
        self.console = Console()
        self.config_file = "wow_bot_config.json"
        self.screenshots_dir = "screenshots"
        
        # Load configuration
        for key, value in DEFAULT_CONFIG.items():
            setattr(self, key, value)
        
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
        
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
        selected_count = len(self.selected_windows)
        panels = [
            Panel(f"{selected_count}", title="Selected", border_style="cyan"),
            Panel(f"{self.base_interval:.1f}s", title="Base interval", border_style="cyan"),
            Panel(f"{self.random_range:.1f}s", title="Random range", border_style="cyan"),
            Panel(Text("on" if self.anti_afk_enabled else "off", 
                      style=f"bold {'green' if self.anti_afk_enabled else 'red'}"), 
                  title="Anti-AFK", border_style="green" if self.anti_afk_enabled else "red"),
            Panel(Text("on" if self.screenshots_enabled else "off", 
                      style=f"bold {'green' if self.screenshots_enabled else 'red'}"), 
                  title="Screenshots", border_style="green" if self.screenshots_enabled else "red"),
            Panel(Text("on" if self.element_detection_enabled else "off", 
                      style=f"bold {'green' if self.element_detection_enabled else 'red'}"), 
                  title="Element Detection", border_style="green" if self.element_detection_enabled else "red"),
        ]
        self.console.print(Columns(panels, equal=True, expand=True))
        self.console.print(Rule(style="grey50"))
        
    def find_wow_windows(self):
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if "World of Warcraft" in window_title or "WoW" in window_title:
                    try:
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        windows.append({'hwnd': hwnd, 'title': window_title, 'pid': pid})
                    except:
                        windows.append({'hwnd': hwnd, 'title': window_title, 'pid': None})
            return True
        
        self.wow_windows = []
        win32gui.EnumWindows(enum_windows_callback, self.wow_windows)
        return self.wow_windows
    
    def select_windows(self):
        if not self.wow_windows:
            self.console.print("[bold red]No WoW windows found![/bold red]")
            return False

        choices = [f"{i+1}. {w['title']}" for i, w in enumerate(self.wow_windows)]
        try:
            picked = questionary.checkbox(
                "Select WoW windows (space to toggle, enter to confirm)",
                choices=choices, qmark=""
            ).ask()
            if not picked:
                self.console.print("[yellow]No windows selected.[/yellow]")
                return False
            
            indices = [int(label.split(".")[0]) - 1 for label in picked 
                      if label.split(".")[0].isdigit()]
            valid_indices = [i for i in indices if 0 <= i < len(self.wow_windows)]
            
            if not valid_indices:
                self.console.print("[yellow]Invalid selection.[/yellow]")
                return False
                
            self.selected_windows = [self.wow_windows[i] for i in valid_indices]
            self.console.print(f"[green]{len(self.selected_windows)} window(s) selected![/green]")
            return True
        except KeyboardInterrupt:
            return False
    
    def switch_to_window(self, window):
        try:
            if win32gui.IsIconic(window['hwnd']):
                win32gui.ShowWindow(window['hwnd'], win32con.SW_RESTORE)
            time.sleep(0.1)
            return True
        except Exception as e:
            print(f"Error preparing window: {e}")
            return False
    
    def send_key(self, hwnd, vk_code, hold_duration=0.1):
        """Send a key press to window"""
        if not self.dry_run:
            win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, vk_code, 0)
            time.sleep(hold_duration)
            win32api.PostMessage(hwnd, win32con.WM_KEYUP, vk_code, 0)
        else:
            time.sleep(hold_duration)
    
    def send_enter_keys(self, hwnd):
        """Send two enter keys with 1 second interval"""
        self.console.print("[bold green]🎯 elemento1.png detectado! Enviando teclas 'enter'...[/bold green]")
        
        self.send_key(hwnd, VK_CODES['ENTER'])
        self.console.print("[green]✅ Primeira tecla 'enter' enviada![/green]")
        
        time.sleep(1.0)
        
        self.send_key(hwnd, VK_CODES['ENTER'])
        self.console.print("[green]✅ Segunda tecla 'enter' enviada![/green]")
    
    def check_for_elements(self, window, max_checks=12):
        """Check for elements in a loop"""
        self.console.print(f"[yellow]⏳ Aguardando {self.wait_after_click}s para procurar elemento2...[/yellow]")
        time.sleep(self.wait_after_click)
        
        for check_count in range(1, max_checks + 1):
            self.console.print(f"[dim]🔍 Verificação {check_count}/{max_checks} - Procurando elementos...[/dim]")
            
            screenshot_path = self.capture_window_screenshot(window)
            if not screenshot_path:
                continue
            
            # Check for elemento1
            element1_detected, element1_info = self.detect_element(screenshot_path, self.element1_template_path)
            if element1_detected:
                self.console.print("[bold green]🎯 elemento1.png detectado novamente! Repetindo ações...[/bold green]")
                self.send_enter_keys(window['hwnd'])
                time.sleep(30.0)
                continue
            
            # Check for elemento2
            element2_detected, element2_info = self.detect_element(screenshot_path, self.element2_template_path)
            if element2_detected:
                self.console.print("[bold green]🎯 elemento2.png detectado! Enviando tecla 'enter'...[/bold green]")
                self.send_key(window['hwnd'], VK_CODES['ENTER'])
                self.console.print("[green]✅ Tecla 'enter' enviada para elemento2![/green]")
                self._cleanup_screenshot(screenshot_path)
                return True, element2_info
            
            self.console.print(f"[dim]🔍 Nenhum elemento encontrado na verificação {check_count}[/dim]")
            self._cleanup_screenshot(screenshot_path)
            
            if check_count < max_checks:
                time.sleep(30.0)
        
        self.console.print(f"[dim]⏰ Timeout: Nenhum elemento encontrado após {max_checks} verificações[/dim]")
        return False, None
    
    def _cleanup_screenshot(self, screenshot_path):
        """Clean up screenshot file"""
        if screenshot_path and os.path.exists(screenshot_path):
            try:
                os.remove(screenshot_path)
            except Exception:
                pass
    
    def send_key_to_window(self, window, key):
        """Main method to send keys and handle element detection"""
        try:
            hwnd = window['hwnd']
            
            # Send '0' key with random hold duration
            hold_duration_0 = random.uniform(0.1, 1.0)
            self.send_key(hwnd, VK_CODES['0'], hold_duration_0)
            time.sleep(0.1)
            
            # Anti-AFK movement
            movement_key = None
            hold_duration_movement = None
            if self.anti_afk_enabled:
                hold_duration_movement = random.uniform(0.1, 0.5)
                movement_options = [('A', VK_CODES['A']), ('D', VK_CODES['D']), 
                                  ('S', VK_CODES['S']), ('W', VK_CODES['W'])]
                movement_key, vk_movement = random.choice(movement_options)
                self.send_key(hwnd, vk_movement, hold_duration_movement)
            
            # Screenshot and element detection
            screenshot_path = None
            element1_detected = False
            element1_info = None
            element2_detected = False
            element2_info = None
            click_performed = False
            
            if self.screenshots_enabled and not self.dry_run:
                screenshot_path = self.capture_window_screenshot(window)
                
                if screenshot_path and self.element_detection_enabled:
                    element1_detected, element1_info = self.detect_element(screenshot_path, self.element1_template_path)
                    
                    if element1_detected:
                        self.send_enter_keys(hwnd)
                        click_performed = True
                        element2_detected, element2_info = self.check_for_elements(window)
            
            # Cleanup screenshot
            if screenshot_path:
                self._cleanup_screenshot(screenshot_path)
                self.console.print(f"[dim]🗑️ Screenshot excluído: {os.path.basename(screenshot_path)}[/dim]")
            
            return True, movement_key, hold_duration_0, hold_duration_movement, \
                   screenshot_path, element1_detected, element1_info, \
                   element2_detected, element2_info, click_performed
                   
        except Exception as e:
            print(f"Error sending key to window: {e}")
            return False, None, None, None, None, False, None, False, None, False
    
    def get_random_interval(self):
        return self.base_interval + random.uniform(0, self.random_range)

    def capture_window_screenshot(self, window):
        """Capture window screenshot without focusing"""
        try:
            hwnd = window['hwnd']
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width, height = right - left, bottom - top
            
            if width <= 0 or height <= 0:
                return None
            
            hwndDC = win32gui.GetWindowDC(hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
            saveDC.SelectObject(saveBitMap)
            
            user32 = ctypes.windll.user32
            user32.PrintWindow.argtypes = [wintypes.HWND, wintypes.HDC, wintypes.UINT]
            user32.PrintWindow.restype = wintypes.BOOL
            
            result = user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
            
            if result:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                window_title = window['title'].replace(":", "_").replace("/", "_").replace("\\", "_")
                filename = f"{timestamp}_{window_title}.png"
                filepath = os.path.join(self.screenshots_dir, filename)
                
                saveBitMap.SaveBitmapFile(saveDC, filepath)
                
                # Cleanup
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwndDC)
                
                return filepath
            else:
                # Cleanup on failure
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(hwnd, hwndDC)
                return None
                
        except Exception as e:
            self.console.print(f"[red]Error capturing screenshot:[/red] {e}")
            return None

    def detect_element(self, screenshot_path, template_path):
        """Generic element detection using OpenCV"""
        try:
            if not self.element_detection_enabled or not os.path.exists(template_path):
                return False, None
            
            screenshot = Image.open(screenshot_path).convert('RGB')
            template = Image.open(template_path).convert('RGB')
            
            screenshot_array = np.array(screenshot)
            template_array = np.array(template)
            
            template_height, template_width = template_array.shape[:2]
            screenshot_height, screenshot_width = screenshot_array.shape[:2]
            
            if template_width > screenshot_width or template_height > screenshot_height:
                return False, None
            
            # Convert to grayscale
            screenshot_gray = cv2.cvtColor(screenshot_array, cv2.COLOR_RGB2GRAY) if len(screenshot_array.shape) == 3 else screenshot_array
            template_gray = cv2.cvtColor(template_array, cv2.COLOR_RGB2GRAY) if len(template_array.shape) == 3 else template_array
            
            # Template matching
            result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= self.detection_threshold:
                template_height, template_width = template_gray.shape
                center_x = max_loc[0] + template_width // 2
                center_y = max_loc[1] + template_height // 2
                
                return True, {
                    'confidence': max_val,
                    'position': (center_x, center_y),
                    'top_left': max_loc,
                    'bottom_right': (max_loc[0] + template_width, max_loc[1] + template_height)
                }
            
            return False, None
            
        except Exception as e:
            self.console.print(f"[red]Error detecting element:[/red] {e}")
            return False, None

    def is_stop_requested(self):
        """Check if F8 is pressed"""
        try:
            state = win32api.GetAsyncKeyState(VK_CODES['F8'])
            return (state & 0x8000) != 0
        except Exception:
            try:
                return keyboard.is_pressed('f8')
            except Exception:
                return False

    def wait_with_stop(self, seconds):
        """Wait with F8 interruption support"""
        end_time = time.time() + seconds
        while time.time() < end_time and self.running:
            if self.is_stop_requested():
                self.console.print("[yellow]Stopping bot and returning to menu...[/yellow]")
                self.running = False
                return True
            time.sleep(0.1)
        return not self.running
        
    def start_bot(self):
        """Start the bot"""
        if not self.selected_windows:
            print("No windows selected! Use the configuration option first.")
            return
        
        self.console.print(Panel.fit(Text("WORLD OF WARCRAFT BOT", justify="center", style="bold white"), 
                                   subtitle="Multiple windows", border_style="cyan"))
        self.console.print(f"Using [bold]{len(self.selected_windows)}[/bold] WoW window(s)")
        
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
                current_window = self.selected_windows[self.current_window_index]
                if self.switch_to_window(current_window):
                    result = self.send_key_to_window(current_window, '0')
                    if result[0]:
                        movement, hold_0, hold_movement, screenshot_path, element1_detected, \
                        element1_info, element2_detected, element2_info, click_performed = result[1:]
                        current_time = time.strftime('%H:%M:%S')
                        
                        # Build status message
                        status_msg = f"[green]✓[/green] '0' ({hold_0:.2f}s)"
                        if movement is not None and hold_movement is not None:
                            status_msg += f" + move '[bold]{movement}[/bold]' ({hold_movement:.2f}s)"
                        status_msg += f" on '[cyan]{current_window['title']}[/cyan]' at {current_time}"
                        
                        if screenshot_path:
                            status_msg += f" [dim]📸 {os.path.basename(screenshot_path)}[/dim]"
                        
                        if element1_detected and element1_info:
                            confidence = element1_info['confidence']
                            position = element1_info['position']
                            status_msg += f" [bold green]🎯 elemento1.png detectado! (conf: {confidence:.2f}, pos: {position})[/bold green]"
                            if click_performed:
                                status_msg += f" [green]✅ Teclas 'enter' enviadas![/green]"
                        elif self.element_detection_enabled:
                            status_msg += f" [dim]🔍 elemento1.png não encontrado[/dim]"
                        
                        if element2_detected and element2_info:
                            confidence2 = element2_info['confidence']
                            position2 = element2_info['position']
                            status_msg += f" [bold blue]🎯 elemento2.png detectado! (conf: {confidence2:.2f}, pos: {position2})[/bold blue]"
                        
                        self.console.print(status_msg)
                    else:
                        self.console.print(f"[red]Error sending keys to:[/red] {current_window['title']}")
                    
                    self.current_window_index = (self.current_window_index + 1) % len(self.selected_windows)
                else:
                    self.console.print(f"[red]Error preparing window:[/red] {current_window['title']}")
                
                next_interval = self.get_random_interval()
                self.console.print(f"Next action in [bold]{next_interval:.1f}s[/bold]")
                
                if self.wait_with_stop(next_interval):
                    break
                
        except KeyboardInterrupt:
            self.console.print("\n[bold yellow]Bot interrompido pelo usuário![/bold yellow]")
        except Exception as e:
            self.console.print(f"[red]Erro:[/red] {e}")
        finally:
            self.stop_bot()

    def test_cycle(self):
        """Single dry-run cycle"""
        if not self.selected_windows:
            print("Configure windows first (option 1)!")
            return
            
        self.console.print(Panel("No keys will be sent. Simulating timings and movements.", 
                               title="TEST (DRY-RUN)", border_style="magenta"))
        original_dry_run = self.dry_run
        self.dry_run = True
        
        try:
            for idx, window in enumerate(self.selected_windows):
                if self.switch_to_window(window):
                    ok, movement, hold_0, hold_move, screenshot_path, element1_detected, \
                    element1_info, element2_detected, element2_info, click_performed = self.send_key_to_window(window, '0')
                    
                    if ok:
                        status_msg = f"[{idx+1}/{len(self.selected_windows)}] '0' ({hold_0:.2f}s) + move '{movement}' ({hold_move:.2f}s) on '[cyan]{window['title']}[/cyan]'"
                        if screenshot_path:
                            status_msg += f" [dim]📸 {os.path.basename(screenshot_path)}[/dim]"
                        if element1_detected and element1_info:
                            confidence = element1_info['confidence']
                            position = element1_info['position']
                            status_msg += f" [bold green]🎯 elemento1.png detectado! (conf: {confidence:.2f}, pos: {position})[/bold green]"
                            if click_performed:
                                status_msg += f" [green]✅ Teclas 'enter' enviadas![/green]"
                        elif self.element_detection_enabled:
                            status_msg += f" [dim]🔍 elemento1.png não encontrado[/dim]"
                        if element2_detected and element2_info:
                            confidence2 = element2_info['confidence']
                            position2 = element2_info['position']
                            status_msg += f" [bold blue]🎯 elemento2.png detectado! (conf: {confidence2:.2f}, pos: {position2})[/bold blue]"
                        self.console.print(status_msg)
                    else:
                        self.console.print(f"[red]Failed to simulate send to:[/red] {window['title']}")
                else:
                    self.console.print(f"[red]Failed to prepare window:[/red] {window['title']}")
        finally:
            self.dry_run = original_dry_run
        self.console.print("[green]Test completed. No actions were sent.[/green]")

    def show_status(self):
        """Display status overview"""
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
        table.add_row("Screenshots", "on" if self.screenshots_enabled else "off")
        table.add_row("Screenshots dir", self.screenshots_dir)
        table.add_row("Element Detection", "on" if self.element_detection_enabled else "off")
        table.add_row("Element1 template", self.element1_template_path)
        table.add_row("Element2 template", self.element2_template_path)
        table.add_row("Detection threshold", f"{self.detection_threshold:.2f}")
        table.add_row("Wait after click", f"{self.wait_after_click:.1f}s")
        self.console.print(table)
    
    def stop_bot(self):
        self.running = False
        self.console.print("[bold]Bot stopped![/bold]")
    
    def set_base_interval(self, seconds):
        self.base_interval = seconds
        self.console.print(f"Base interval set to [bold]{seconds}[/bold] seconds")
        self.console.print(f"Total between [bold]{seconds}-{seconds + self.random_range}[/bold] seconds")
        self.save_configuration()
    
    def set_random_range(self, seconds):
        self.random_range = seconds
        self.console.print(f"Random range set to [bold]{seconds}[/bold] seconds")
        self.console.print(f"Total between [bold]{self.base_interval}-{self.base_interval + seconds}[/bold] seconds")
        self.save_configuration()

    def set_anti_afk_enabled(self, enabled):
        self.anti_afk_enabled = bool(enabled)
        state = "on" if self.anti_afk_enabled else "off"
        self.console.print(f"Anti-AFK is now [bold]{state}[/bold].")
        self.save_configuration()
    
    def set_screenshots_enabled(self, enabled):
        self.screenshots_enabled = bool(enabled)
        state = "on" if self.screenshots_enabled else "off"
        self.console.print(f"Screenshots are now [bold]{state}[/bold].")
        if self.screenshots_enabled:
            self.console.print(f"Screenshots will be saved to: [cyan]{self.screenshots_dir}[/cyan]")
        self.save_configuration()
    
    def set_element_detection_enabled(self, enabled):
        self.element_detection_enabled = bool(enabled)
        state = "on" if self.element_detection_enabled else "off"
        self.console.print(f"Element detection is now [bold]{state}[/bold].")
        if self.element_detection_enabled:
            self.console.print(f"Looking for element1: [cyan]{self.element1_template_path}[/cyan]")
            self.console.print(f"Looking for element2: [cyan]{self.element2_template_path}[/cyan]")
            self.console.print(f"Detection threshold: [cyan]{self.detection_threshold:.2f}[/cyan]")
            self.console.print(f"Wait after click: [cyan]{self.wait_after_click:.1f}s[/cyan]")
        self.save_configuration()
    
    def save_configuration(self):
        try:
            config = {key: getattr(self, key) for key in DEFAULT_CONFIG.keys()}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            self.console.print(f"✅ Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            self.console.print(f"❌ Erro ao salvar configuração: {e}")
            return False
    
    def load_configuration(self):
        try:
            if not os.path.exists(self.config_file):
                return False
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            for key in DEFAULT_CONFIG.keys():
                if key in config:
                    setattr(self, key, config[key])
            
            return True
        except Exception:
            return False
    
    def configure_windows(self):
        with self.console.status("Searching for World of Warcraft windows...", spinner="dots"):
            self.find_wow_windows()
        
        if not self.wow_windows:
            self.console.print("[red]No WoW windows found![/red]")
            self.console.print("Make sure World of Warcraft is running.")
            return False
        
        return self.select_windows()

def main():
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
            bot.console.clear()
            bot.render_header()
            bot.render_quick_status()
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    "Configure WoW windows",
                    "Start bot",
                    "Anti-AFK (on/off)",
                    "Screenshots (on/off)",
                    "Element Detection (on/off)",
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
            elif action == "Screenshots (on/off)":
                bot.set_screenshots_enabled(not bot.screenshots_enabled)
            elif action == "Element Detection (on/off)":
                bot.set_element_detection_enabled(not bot.element_detection_enabled)
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