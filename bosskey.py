"""
BossKey - System Tray Window Hider
Hides/shows selected windows with a configurable global hotkey.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
from typing import Optional

import keyboard
import pystray
import win32con
import win32gui
import win32process
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
ICON_PNG = os.path.join(BASE_DIR, "bosskey_icon.png")

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
DEFAULT_CONFIG: dict = {
    "hotkey": "ctrl+shift+b",
    "pinned_windows": [],          # list of exe names to auto-manage
    "start_minimised": True,
}

# ---------------------------------------------------------------------------
# Color palette (dark premium theme)
# ---------------------------------------------------------------------------
BG      = "#0d1117"
BG2     = "#161b22"
BG3     = "#21262d"
ACCENT  = "#00d4ff"
ACCENT2 = "#0099bb"
TEXT    = "#e6edf3"
TEXT2   = "#8b949e"
DANGER  = "#f85149"
SUCCESS = "#3fb950"
BORDER  = "#30363d"


# ===========================================================================
# Config helpers
# ===========================================================================

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {**DEFAULT_CONFIG, **data}
        except Exception:
            pass
    return dict(DEFAULT_CONFIG)


def save_config(cfg: dict) -> None:
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)


# ===========================================================================
# Windows enumeration helpers
# ===========================================================================

def get_visible_windows() -> list[dict]:
    """Return a list of dicts for all visible, titled, non-system windows."""
    results: list[dict] = []

    def _enum(hwnd: int, _: None) -> bool:
        if not win32gui.IsWindowVisible(hwnd):
            return True
        title = win32gui.GetWindowText(hwnd)
        if not title.strip():
            return True
        # Skip taskbar, shell, etc.
        class_name = win32gui.GetClassName(hwnd)
        if class_name in ("Shell_TrayWnd", "Progman", "WorkerW"):
            return True
        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            import psutil  # optional – fall back gracefully
            exe = psutil.Process(pid).name()
        except Exception:
            exe = "unknown.exe"
        results.append({"hwnd": hwnd, "title": title, "exe": exe})
        return True

    win32gui.EnumWindows(_enum, None)
    return results


def hide_window(hwnd: int) -> None:
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)


def show_window(hwnd: int) -> None:
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.SetForegroundWindow(hwnd)


# ===========================================================================
# BossKey Engine
# ===========================================================================

class BossKeyEngine:
    """Core logic: track hidden windows and handle the toggle hotkey."""

    def __init__(self, config: dict) -> None:
        self.config = config
        self._hidden: dict[int, str] = {}   # hwnd → title
        self._lock = threading.Lock()
        self._hotkey_registered = False

    # ------------------------------------------------------------------
    # Hotkey management
    # ------------------------------------------------------------------

    def register_hotkey(self) -> None:
        if self._hotkey_registered:
            try:
                keyboard.remove_hotkey(self.config["hotkey"])
            except Exception:
                pass
        keyboard.add_hotkey(self.config["hotkey"], self._on_hotkey, suppress=True)
        self._hotkey_registered = True

    def update_hotkey(self, new_hotkey: str) -> None:
        if self._hotkey_registered:
            try:
                keyboard.remove_hotkey(self.config["hotkey"])
            except Exception:
                pass
        self.config["hotkey"] = new_hotkey
        keyboard.add_hotkey(new_hotkey, self._on_hotkey, suppress=True)
        self._hotkey_registered = True

    def stop(self) -> None:
        if self._hotkey_registered:
            try:
                keyboard.remove_all_hotkeys()
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Toggle
    # ------------------------------------------------------------------

    def _on_hotkey(self) -> None:
        def _task():
            with self._lock:
                if self._hidden:
                    self._restore_all()
                else:
                    self._hide_targets()
        threading.Thread(target=_task, daemon=True).start()

    def _hide_targets(self) -> None:
        """Hide windows currently tracked OR all visible app windows."""
        targets = self._get_target_hwnds()
        for hwnd, title in targets:
            hide_window(hwnd)
            self._hidden[hwnd] = title

    def _restore_all(self) -> None:
        for hwnd, _title in list(self._hidden.items()):
            try:
                show_window(hwnd)
            except Exception:
                pass
        self._hidden.clear()

    def _get_target_hwnds(self) -> list[tuple[int, str]]:
        """
        Return (hwnd, title) pairs for windows that should be hidden.
        Matches by executable name to ensure reliability even when window titles change
        (e.g. when a new video is played or a new tab is opened).
        """
        selected_exes = {e.lower() for e in self.config.get("selected_exes", [])}
        visible = get_visible_windows()

        if selected_exes:
            return [(w["hwnd"], w["title"]) for w in visible
                    if w["exe"].lower() in selected_exes]
        # No selection → hide everything visible (full boss-mode)
        return [(w["hwnd"], w["title"]) for w in visible]

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    @property
    def is_hidden(self) -> bool:
        return bool(self._hidden)

    @property
    def hidden_count(self) -> int:
        return len(self._hidden)


# ===========================================================================
# Tray Icon helpers
# ===========================================================================

def _load_tray_icon() -> Image.Image:
    """Load the PNG icon or fall back to a generated one."""
    if os.path.exists(ICON_PNG):
        img = Image.open(ICON_PNG).convert("RGBA")
        return img.resize((64, 64), Image.LANCZOS)
    # Fallback: draw a simple key shape
    img = Image.new("RGBA", (64, 64), (13, 17, 23, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 36, 36], outline=(0, 212, 255), width=3)
    draw.rectangle([32, 20, 56, 26], fill=(0, 212, 255))
    draw.rectangle([48, 20, 54, 30], fill=(0, 212, 255))
    draw.rectangle([42, 20, 48, 28], fill=(0, 212, 255))
    return img


# ===========================================================================
# Settings / Window-picker GUI
# ===========================================================================

class BossKeyGUI:
    """Main settings window (opened from tray or on first launch)."""

    def __init__(self, engine: BossKeyEngine, tray_icon: pystray.Icon) -> None:
        self.engine = engine
        self.tray = tray_icon
        self.root: Optional[tk.Tk] = None
        self._hotkey_var: Optional[tk.StringVar] = None
        self._window_vars: dict[str, tk.BooleanVar] = {}  # title → BooleanVar
        self._visible_windows: list[dict] = []
        # Hotkey recording state
        self._recording = False
        self._pressed_keys: list[str] = []      # ordered modifiers + trigger key
        self._rec_hooks: list = []               # keyboard hook handles
        self._hk_entry: Optional[tk.Entry] = None
        self._rec_indicator: Optional[tk.Label] = None

    # ------------------------------------------------------------------
    # Build / open
    # ------------------------------------------------------------------

    def open(self) -> None:
        """Show the settings window; create it on first call, un-hide it on subsequent calls."""
        if self.root and self.root.winfo_exists():
            # Window already built – just bring it back from the tray
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            return

        root = tk.Tk()
        self.root = root
        root.title("BossKey – Settings")
        root.configure(bg=BG)
        root.resizable(False, False)
        root.geometry("520x640")

        # Centre on screen
        root.update_idletasks()
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        w, h = 520, 640
        root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

        # Icon
        if os.path.exists(ICON_PNG):
            try:
                ico = tk.PhotoImage(file=ICON_PNG)
                root.iconphoto(True, ico)
            except Exception:
                pass

        self._build_ui(root)
        # X button → hide to tray, not exit
        root.protocol("WM_DELETE_WINDOW", self._on_close)
        # Minimize button → hide to tray
        root.bind("<Unmap>", self._on_minimize)
        root.mainloop()

    def _on_close(self) -> None:
        """Hide to tray instead of destroying."""
        if self._recording:
            self._stop_recording()
        if self.root:
            self.root.withdraw()

    def _on_minimize(self, event: tk.Event) -> None:
        """Intercept the minimize button and send the window to tray."""
        # event.widget is the root only for the top-level unmap
        if event.widget is self.root:
            self.root.withdraw()

    # ------------------------------------------------------------------
    # UI Construction
    # ------------------------------------------------------------------

    def _build_ui(self, root: tk.Tk) -> None:
        self._style(root)

        # ── Header ────────────────────────────────────────────────────
        header = tk.Frame(root, bg=BG, pady=16)
        header.pack(fill="x", padx=20)

        tk.Label(
            header, text="🔑  BossKey", font=("Segoe UI", 20, "bold"),
            bg=BG, fg=ACCENT,
        ).pack(side="left")

        tk.Label(
            header, text="Window hider for the sneaky boss situation",
            font=("Segoe UI", 9), bg=BG, fg=TEXT2,
        ).pack(side="left", padx=(12, 0), pady=(6, 0))

        # ── Divider ───────────────────────────────────────────────────
        tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=20)

        # ── Status badge ──────────────────────────────────────────────
        status_frame = tk.Frame(root, bg=BG, pady=12)
        status_frame.pack(fill="x", padx=20)

        self._status_label = tk.Label(
            status_frame, text="● VISIBLE", font=("Segoe UI", 11, "bold"),
            bg=BG, fg=SUCCESS,
        )
        self._status_label.pack(side="left")

        self._count_label = tk.Label(
            status_frame, text="", font=("Segoe UI", 9), bg=BG, fg=TEXT2,
        )
        self._count_label.pack(side="left", padx=8)

        # Manual toggle button
        tk.Button(
            status_frame, text="Toggle Now",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT2, fg="white", relief="flat",
            activebackground=ACCENT, activeforeground="white",
            padx=12, pady=4, cursor="hand2",
            command=self._manual_toggle,
        ).pack(side="right")

        # ── Hotkey section ────────────────────────────────────────────
        self._section_label(root, "⌨  Hotkey")
        hk_frame = tk.Frame(root, bg=BG2, padx=16, pady=12)
        hk_frame.pack(fill="x", padx=20, pady=(0, 8))

        # Label row: title + live REC indicator
        hk_title_row = tk.Frame(hk_frame, bg=BG2)
        hk_title_row.pack(fill="x")
        tk.Label(hk_title_row, text="Keyboard shortcut:",
                 font=("Segoe UI", 9), bg=BG2, fg=TEXT2).pack(side="left")
        self._rec_indicator = tk.Label(
            hk_title_row, text="",
            font=("Segoe UI", 8, "bold"), bg=BG2, fg=DANGER,
        )
        self._rec_indicator.pack(side="left", padx=(10, 0))

        hk_row = tk.Frame(hk_frame, bg=BG2)
        hk_row.pack(fill="x", pady=(4, 0))

        self._hotkey_var = tk.StringVar(value=self.engine.config["hotkey"])
        self._hk_entry = tk.Entry(
            hk_row, textvariable=self._hotkey_var,
            font=("Consolas", 11), bg=BG3, fg=ACCENT,
            insertbackground=ACCENT, relief="flat",
            bd=0, highlightthickness=1, highlightbackground=BORDER,
            highlightcolor=ACCENT,
            cursor="hand2", state="readonly",
        )
        self._hk_entry.pack(side="left", fill="x", expand=True, ipady=6)

        # Clicking the entry starts recording
        self._hk_entry.bind("<Button-1>", lambda e: self._start_recording())

        tk.Button(
            hk_row, text="Apply",
            font=("Segoe UI", 9, "bold"),
            bg=ACCENT2, fg="white", relief="flat",
            activebackground=ACCENT, activeforeground="white",
            padx=10, pady=4, cursor="hand2",
            command=self._apply_hotkey,
        ).pack(side="left", padx=(8, 0))

        tk.Label(
            hk_frame,
            text="Click the field above, then press a single key (e.g. F12, Pause, Scroll Lock).",
            font=("Segoe UI", 8), bg=BG2, fg=TEXT2,
        ).pack(anchor="w", pady=(4, 0))

        # ── Window picker ─────────────────────────────────────────────
        self._section_label(root, "🪟  Windows to hide (leave empty = hide all)")

        picker_outer = tk.Frame(root, bg=BG2, padx=8, pady=8)
        picker_outer.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        # Refresh button
        refresh_btn = tk.Button(
            picker_outer, text="⟳  Refresh window list",
            font=("Segoe UI", 9), bg=BG3, fg=ACCENT,
            relief="flat", activebackground=BG3, activeforeground=ACCENT,
            cursor="hand2", command=self._refresh_windows,
        )
        refresh_btn.pack(anchor="e", pady=(0, 6))

        # Scrollable list
        list_frame = tk.Frame(picker_outer, bg=BG2)
        list_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(list_frame, bg=BG2, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self._window_frame = tk.Frame(canvas, bg=BG2)

        self._window_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self._window_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self._refresh_windows()

        # ── Footer ────────────────────────────────────────────────────
        tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=20)
        footer = tk.Frame(root, bg=BG, pady=12)
        footer.pack(fill="x", padx=20)

        tk.Button(
            footer, text="Save & Close",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT, fg=BG, relief="flat",
            activebackground=ACCENT2, activeforeground=BG,
            padx=20, pady=6, cursor="hand2",
            command=self._save_and_close,
        ).pack(side="right")

        tk.Button(
            footer, text="Clear selection",
            font=("Segoe UI", 9),
            bg=BG3, fg=TEXT2, relief="flat",
            activebackground=BORDER, activeforeground=TEXT,
            padx=12, pady=6, cursor="hand2",
            command=self._clear_selection,
        ).pack(side="right", padx=(0, 8))

        tk.Label(
            footer,
            text=f"Hotkey: {self.engine.config['hotkey']}",
            font=("Segoe UI", 8), bg=BG, fg=TEXT2,
        ).pack(side="left")

        # Start status update loop
        self._update_status()

    def _style(self, root: tk.Tk) -> None:
        style = ttk.Style(root)
        style.theme_use("default")
        style.configure(
            "Vertical.TScrollbar",
            background=BG3, troughcolor=BG2,
            arrowcolor=TEXT2, bordercolor=BG2,
        )

    def _section_label(self, parent: tk.Widget, text: str) -> None:
        tk.Label(
            parent, text=text,
            font=("Segoe UI", 10, "bold"),
            bg=BG, fg=TEXT,
            anchor="w",
        ).pack(fill="x", padx=20, pady=(10, 4))

    # ------------------------------------------------------------------
    # Window list
    # ------------------------------------------------------------------

    def _refresh_windows(self) -> None:
        # Clear old checkboxes
        for widget in self._window_frame.winfo_children():
            widget.destroy()
        self._window_vars.clear()

        self._visible_windows = get_visible_windows()
        selected_exes = {e.lower() for e in self.engine.config.get("selected_exes", [])}

        # Deduplicate: one checkbox row per unique exe
        seen_exes: set[str] = set()
        
        # Exclude our own app
        own_pid = os.getpid()

        for w in self._visible_windows:
            # We don't have PID in w directly, but we don't want to hide ourselves.
            # We'll just exclude python.exe/bosskey.exe if it matches our title.
            if w["title"] == "BossKey – Settings":
                continue

            exe_key = w["exe"].lower()
            if exe_key in seen_exes:
                continue
            seen_exes.add(exe_key)

            var = tk.BooleanVar(value=exe_key in selected_exes)
            self._window_vars[exe_key] = var

            row = tk.Frame(self._window_frame, bg=BG2)
            row.pack(fill="x", padx=4, pady=2)

            cb = tk.Checkbutton(
                row, variable=var,
                bg=BG2, fg=TEXT, selectcolor=BG3,
                activebackground=BG2, activeforeground=ACCENT,
                relief="flat", cursor="hand2",
                command=self._autosave,
            )
            cb.pack(side="left")

            # App executable name
            tk.Label(
                row, text=f"{w['exe']}",
                font=("Consolas", 10, "bold"), bg=BG2, fg=ACCENT2, anchor="w",
            ).pack(side="left", padx=(0, 6))

            # Window count
            count = sum(1 for x in self._visible_windows if x["exe"].lower() == exe_key)
            title_sample = w["title"][:40] + "…" if len(w["title"]) > 40 else w["title"]
            
            info_text = f"({count} window{'s' if count != 1 else ''}) - e.g. {title_sample}"
            tk.Label(
                row, text=info_text,
                font=("Segoe UI", 9), bg=BG2, fg=TEXT2, anchor="w",
            ).pack(side="left", fill="x", expand=True)

    def _clear_selection(self) -> None:
        for var in self._window_vars.values():
            var.set(False)

    # ------------------------------------------------------------------
    # Hotkey recording
    # ------------------------------------------------------------------

    # Canonical modifier names the keyboard library uses
    _MODIFIERS = {"ctrl", "shift", "alt", "windows", "left ctrl", "right ctrl",
                  "left shift", "right shift", "left alt", "right alt"}

    @staticmethod
    def _canonical(name: str) -> str:
        """Normalise key name to a clean keyboard-lib token."""
        name = name.lower()
        aliases = {
            "left ctrl": "ctrl", "right ctrl": "ctrl",
            "left shift": "shift", "right shift": "shift",
            "left alt": "alt", "right alt": "alt",
            "left windows": "windows", "right windows": "windows",
        }
        return aliases.get(name, name)

    def _start_recording(self) -> None:
        if self._recording:
            return
        self._recording = True

        # Visual feedback
        self._hk_entry.config(
            highlightbackground=DANGER, highlightcolor=DANGER,
            highlightthickness=2,
        )
        self._hotkey_var.set("Press a key…")
        if self._rec_indicator:
            self._rec_indicator.config(text="● REC")

        # Temporarily suspend the global boss-key hotkey so it doesn't fire
        self.engine.stop()

        # Only a key-down hook — we finalize on the first key pressed
        self._rec_hooks = [
            keyboard.on_press(self._on_key_down),
        ]

    def _stop_recording(self) -> None:
        if not self._recording:
            return
        self._recording = False

        # Remove capture hooks
        for h in self._rec_hooks:
            try:
                keyboard.unhook(h)
            except Exception:
                pass
        self._rec_hooks.clear()

        # Restore visual state
        self._hk_entry.config(
            highlightbackground=BORDER, highlightcolor=ACCENT,
            highlightthickness=1,
        )
        if self._rec_indicator:
            self._rec_indicator.config(text="")

        # Re-register whatever hotkey is now in the field
        new_hk = self._hotkey_var.get().strip()
        if new_hk and new_hk != "Press keys…":
            try:
                self.engine.update_hotkey(new_hk)
            except Exception:
                pass
        else:
            # Revert to previous
            self._hotkey_var.set(self.engine.config["hotkey"])
            self.engine.register_hotkey()

    def _on_key_down(self, event: keyboard.KeyboardEvent) -> None:
        """Capture the first key pressed and immediately finalize."""
        if not self._recording:
            return
        key = self._canonical(event.name)
        if self.root:
            self.root.after(0, lambda k=key: self._hotkey_var.set(k))
            self.root.after(0, self._stop_recording)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _apply_hotkey(self) -> None:
        new_hk = self._hotkey_var.get().strip()
        if not new_hk:
            messagebox.showwarning("BossKey", "Hotkey cannot be empty.", parent=self.root)
            return
        try:
            self.engine.update_hotkey(new_hk)
            self.engine.config["hotkey"] = new_hk
            save_config(self.engine.config)
            messagebox.showinfo("BossKey", f"Hotkey updated to:\n{new_hk}", parent=self.root)
        except Exception as e:
            messagebox.showerror("BossKey", f"Invalid hotkey: {e}", parent=self.root)

    def _autosave(self) -> None:
        """Persist the current checkbox state immediately."""
        selected_exes = [exe for exe, var in self._window_vars.items() if var.get()]
        self.engine.config["selected_exes"] = selected_exes
        save_config(self.engine.config)

    def _save_and_close(self) -> None:
        self._autosave()
        self._on_close()

    def _manual_toggle(self) -> None:
        self.engine._on_hotkey()

    def _update_status(self) -> None:
        if not self.root or not self.root.winfo_exists():
            return
        # Still schedule next tick even when withdrawn; just skip the UI update
        if self.root.winfo_viewable():
            if self.engine.is_hidden:
                self._status_label.config(text="● HIDDEN", fg=DANGER)
                self._count_label.config(text=f"({self.engine.hidden_count} window(s) hidden)")
            else:
                self._status_label.config(text="● VISIBLE", fg=SUCCESS)
                self._count_label.config(text="")
        self.root.after(500, self._update_status)


# ===========================================================================
# System Tray
# ===========================================================================

def build_menu(engine: BossKeyEngine, gui_ref: list) -> pystray.Menu:
    def _open_settings():
        def _run():
            gui_ref[0].open()
        threading.Thread(target=_run, daemon=True).start()

    def _toggle(_icon, _item):
        engine._on_hotkey()

    def _quit(icon, _item):
        engine.stop()
        engine._restore_all()    # Restore all hidden windows on exit
        icon.stop()

    return pystray.Menu(
        pystray.MenuItem("BossKey", None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(
            lambda _: "🔓 Show windows" if engine.is_hidden else "🔒 Hide windows",
            _toggle,
        ),
        pystray.MenuItem("⚙  Settings…", lambda i, _: _open_settings()),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("✖  Quit", _quit),
    )


def run_tray(engine: BossKeyEngine, gui_ref: list) -> None:
    icon_img = _load_tray_icon()
    menu = build_menu(engine, gui_ref)
    tray = pystray.Icon(
        name="BossKey",
        icon=icon_img,
        title=f"BossKey  [{engine.config['hotkey']}]",
        menu=menu,
    )

    # Give gui_ref[0] access to tray so it can reference it
    gui_ref[0].tray = tray

    tray.run()


# ===========================================================================
# Entry point
# ===========================================================================

def main() -> None:
    config = load_config()
    engine = BossKeyEngine(config)
    engine.register_hotkey()

    # gui_ref allows the tray callback to open the GUI in a thread-safe way
    gui_ref: list[BossKeyGUI] = [BossKeyGUI(engine, None)]  # tray set later

    if not config.get("start_minimised", True):
        threading.Thread(target=gui_ref[0].open, daemon=True).start()

    run_tray(engine, gui_ref)


if __name__ == "__main__":
    main()
