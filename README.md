# 🔑 BossKey

> Hide and show any windows instantly with a keyboard shortcut — lives quietly in the system tray.

![BossKey icon](bosskey_icon.png)

---

## Features

- **Global hotkey** — press once to hide selected windows, press again to restore them
- **Window picker** — choose exactly which windows to hide, or leave empty to hide everything visible
- **System tray** — runs silently in the background; right-click tray icon for menu
- **Persistent config** — settings saved to `config.json`
- **Dark premium UI** — sleek dark settings panel built with tkinter
- **Safe exit** — all hidden windows are restored when BossKey quits

---

## Quick Start

### 1. Setup environment (first time only)

```bat
setup_venv.bat
```

### 2. Run BossKey

```bat
run.bat          # silent (no console window)
run_debug.bat    # with console for log output
```

---

## Default Hotkey

`Ctrl + Shift + B`

Change it anytime via **Settings → Hotkey → Apply**.

---

## How it works

| Action | Result |
|---|---|
| Press hotkey (windows visible) | Hides selected / all windows |
| Press hotkey again (windows hidden) | Restores all hidden windows |
| Tray → "Show/Hide windows" | Same as hotkey |
| Tray → "Settings…" | Open settings GUI |
| Tray → "Quit" | Restore all windows and exit |

---

## Project Structure

```
bosskey/
├── bosskey.py        # Main application
├── bosskey_icon.png  # App icon (PNG)
├── convert_icon.py   # PNG → ICO converter utility
├── config.json       # Runtime config (auto-created)
├── requirements.txt  # Python dependencies
├── setup_venv.bat    # One-time environment setup
├── run.bat           # Silent launcher
├── run_debug.bat     # Debug launcher (shows console)
└── venv/             # Isolated virtual environment
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `pystray` | System tray icon |
| `keyboard` | Global hotkey listener |
| `pywin32` | Windows API (hide/show windows) |
| `Pillow` | Image handling for tray icon |
| `psutil` | Process name resolution |

---

## Configuration (`config.json`)

```json
{
  "hotkey": "ctrl+shift+b",
  "selected_hwnds": [],
  "pinned_windows": [],
  "start_minimised": true
}
```

- `hotkey` — keyboard shortcut string
- `selected_hwnds` — specific window handles to manage (set via GUI)
- `pinned_windows` — list of exe names to always target (e.g. `["chrome.exe"]`)
- `start_minimised` — if `true`, starts without showing settings window

---

## Requirements

- Windows 10 / 11
- Python 3.9+
