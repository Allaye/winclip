# clipboard_manager/main.py
import time
from winclip.engine.monitor import ClipboardMonitor
from winclip.engine.storage import get_recent_clips, init_db, insert_clip
from winclip.engine.model import Clip

def handle_clipboard_change(text):
    print(f"[+] New clipboard text:\n{text}\n")
    clip = Clip(content=text)
    init_db()  # Ensure the database is initialized
    insert_clip(clip)

    clips = get_recent_clips(2)
    for clip in clips:
        print(f"{clip.timestamp} - {clip.content[:30]}... (pinned={clip.pinned})")


if __name__ == "__main__":
    monitor = ClipboardMonitor(on_clipboard_change=handle_clipboard_change)
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
        print("Clipboard monitor stopped.")



