# clipboard_manager/main.py
import time
from engine.monitor import ClipboardMonitor
from engine.storage import get_recent_clips, init_db, insert_clip
from engine.model import Clip
from gi.repository import GLib
from gui.app import launch_gui

# def handle_clipboard_change(text):
#     print(f"[+] New clipboard text:\n{text}\n")
#     clip = Clip(content=text)
#     # init_db()  # Ensure the database is initialized
#     insert_clip(clip)

#     clips = get_recent_clips(2)
#     for clip in clips:
#         print(f"{clip.timestamp} - {clip.content[:30]}... (pinned={clip.pinned})")


# if __name__ == "__main__":
#     monitor = ClipboardMonitor(on_clipboard_change=handle_clipboard_change)
#     monitor.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         monitor.stop()
#         print("Clipboard monitor stopped.")




# Global-like window reference
window_ref = {}

def update_ui(text):
    clip = Clip(content=text)
    insert_clip(clip)
    
    if "win" in window_ref:
        window_ref["win"].refresh_clips()  # Ensure your ClipboardWindow has this method

    return False  # Required for GLib.idle_add

def on_clipboard_change(text):
    GLib.idle_add(update_ui, text)

if __name__ == "__main__":
    # Start clipboard monitor
    monitor = ClipboardMonitor(on_clipboard_change=on_clipboard_change)
    monitor.start()

    # Launch the GUI and keep reference to main window
    win = launch_gui()
    print(f"GUI launched, main window reference stored: {win}")
    window_ref["win"] = win

