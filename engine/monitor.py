"""Background clipboard polling monitor."""

import subprocess
import threading
import time
import engine.storage as storage


class ClipboardMonitor:
    """Poll the system clipboard and fire a callback on changes.

    Attributes:
        on_clipboard_change: Callback invoked with the new text.
        poll_interval: Seconds between clipboard reads.
    """

    def __init__(self, on_clipboard_change, poll_interval=1.0):
        """Initialise the monitor.

        Args:
            on_clipboard_change: Callable that receives new clipboard text.
            poll_interval: Seconds between polls.
        """

        self.on_clipboard_change = on_clipboard_change
        self.poll_interval = poll_interval
        self._running = False
        self._last_clipboard = None
        storage.init_db()

    def _read_clipboard(self):
        """Read the current system clipboard via ``xclip``.

        Returns:
            The clipboard text, or None on failure.
        """
        try:
            result = subprocess.run(
                ['xclip', '-selection', 'clipboard', '-o'],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )
            return result.stdout.strip()
        except Exception:
            return None

    def _monitor_loop(self):
        """Continuously poll the clipboard until stopped."""
        while self._running:
            current = self._read_clipboard()
            if current and current != self._last_clipboard:
                self._last_clipboard = current
                self.on_clipboard_change(current)
            time.sleep(self.poll_interval)

    def start(self):
        """Start polling in a background daemon thread."""
        self._running = True
        threading.Thread(target=self._monitor_loop, daemon=True).start()

    def stop(self):
        """Signal the polling loop to stop."""
        self._running = False

    
