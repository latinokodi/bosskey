# 🔑 BossKey

> Hide and show any windows instantly with a keyboard shortcut — lives quietly in the system tray.

![BossKey icon](bosskey_icon.png)

---

## Features

- **Single-key hotkey** — assign any key (F12, Pause, etc.) to toggle visibility instantly.
- **Title-based selection** — choose exactly which windows to hide by their visible titles.
- **Auto-save** — selections are saved immediately as you toggle them.
- **System tray** — runs silently; right-click tray icon for menu or to open settings.
- **Minimize to tray** — closing or minimizing the settings window hides it to the tray.
- **Dark premium UI** — sleek dark mode settings panel built with tkinter.
- **Safe exit** — all hidden windows are restored when BossKey quits.

---

## Quick Start

### 1. Run BossKey

Just run the batch file. It will automatically create the virtual environment, install dependencies, and start the app.

```bat
run.bat          # silent (no console window)
run_debug.bat    # with console for log output
```

---

## How it works

| Action | Result |
|---|---|
| Click Hotkey Field | Enter "Recording" mode to assign a new key |
| Press assigned key | Toggle visibility of selected windows |
| Tray → "Show/Hide windows" | Same as hotkey |
| Tray → "Settings…" | Open settings GUI |
| Tray → "Quit" | Restore all windows and exit |

---

## Project Structure

```
bosskey/
├── bosskey.py        # Main application
├── bosskey_icon.png  # App icon
├── config.json       # Runtime config (auto-created)
├── requirements.txt  # Python dependencies
├── run.bat           # Auto-setup & Silent launcher
├── run_debug.bat     # Auto-setup & Debug launcher
└── venv/             # Isolated virtual environment (auto-created)
```

---

## Configuration (`config.json`)

```json
{
  "hotkey": "scroll lock",
  "selected_titles": [],
  "start_minimised": true
}
```

- `hotkey` — single key name
- `selected_titles` — list of window titles to manage
- `start_minimised` — if `true`, starts without showing settings window

---

## Requirements

- Windows 10 / 11
- Python 3.9+

