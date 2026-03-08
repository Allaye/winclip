# gui/app.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore[import-untyped]\
from gi.repository import GLib # type: ignore[import-untyped]
from engine.monitor import ClipboardMonitor
from engine.storage import insert_clip
from engine.model import Clip
from .winclip import ClipboardWindow
from .styles import style


def update_ui(text, win):
    clip = Clip(content=text)
    insert_clip(clip)
    
    if win:
        win.refresh_clips()

    return False  # Required for GLib.idle_add


def launch_gui():
    # Use a simple application ID
    app = Gtk.Application(application_id="com.allaye.winclip")

    def on_activate(app):
        try:

            win = ClipboardWindow(application=app)
            style.load_css(app)  # Load CSS after window creation
            win.present()

            def on_clipboard_change(text):
                GLib.idle_add(update_ui, text, win)
            
            monitor = ClipboardMonitor(on_clipboard_change=on_clipboard_change)
            monitor.start()
            # window_holder["win"] = win
        except Exception as e:
            print(f"Error in on_activate: {e}")
            import traceback
            traceback.print_exc()
            app.quit()

    def on_startup(app):
        print("Application starting up...")

    app.connect("activate", on_activate)
    app.connect("startup", on_startup)
    
    try:
        # Use run with None instead of empty list - this is important for GTK4
        exit_status = app.run(None)
        print(f"Application exited with status: {exit_status}")
        return app
    except Exception as e:
        print(f"Failed to run application: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        # Clean up any remaining processes
        app.quit()