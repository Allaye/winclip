"""Background clipboard polling monitor."""

import subprocess
import threading
import time
import engine.storage as storage

class ClipboardMonitor:
    def __init__(self, on_clipboard_change, poll_interval=1.0):
        self.on_clipboard_change = on_clipboard_change
        self.poll_interval = poll_interval
        self._running = False
        self._last_clipboard = None
        storage.init_db()

    def _read_clipboard(self):
        try:
            import os
            if os.environ.get("WAYLAND_DISPLAY"):
                result = subprocess.run(['wl-paste', '-n'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
            
            result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            return result.stdout.strip()
        except Exception:
            return None

    def _monitor_loop(self):
        while self._running:
            current = self._read_clipboard()
            if current and current != self._last_clipboard:
                self._last_clipboard = current
                self.on_clipboard_change(current)
            time.sleep(self.poll_interval)

    def start(self):
        self._running = True
        threading.Thread(target=self._monitor_loop, daemon=True).start()

    def stop(self):
        self._running = False
