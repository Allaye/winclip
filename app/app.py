# gui/app.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore[import-untyped]\
from gi.repository import GLib # type: ignore[import-untyped]
from engine.monitor import ClipboardMonitor
from engine.storage import insert_clip
from engine.model import Clip
from app.winclip import ClipboardWindow
from gui.styles import style


def update_ui(text, win):
    clip = Clip(content=text)
    insert_clip(clip)
    
    if win:
        win.refresh_clips()

    return False  # Required for GLib.idle_add


def start_app(hide_gui=False):
    # Use a simple application ID
    app = Gtk.Application(application_id="com.allaye.winclip")

    def on_activate(app):
        try:
            if app.win is None:
                app.win = ClipboardWindow(application=app)
            should_present = not app.hide_gui
            app.hide_gui = False

            if should_present:
                app.win.present()
        except Exception as e:
            print(f"Error in on_activate: {e}")
            import traceback
            traceback.print_exc()
            app.quit()

    def on_startup(app):
        print("Application starting up...")
        app.win = None  # Placeholder for window reference
        app.monitor = None  # Placeholder for monitor reference
        app.hide_gui = hide_gui  # Store the hide_gui flag in the app instance
        style.load_css(app)  # Load CSS on startup to ensure styles are available

        def on_clipboard_change(text):
            GLib.idle_add(update_ui, text, app.win)  # Pass None for win, will update UI on next refresh

        app.monitor = ClipboardMonitor(on_clipboard_change=on_clipboard_change)
        app.monitor.start()

    def on_shutdown(app):
        if app.monitor is not None:
            app.monitor.stop()

    app.connect("startup", on_startup)
    app.connect("activate", on_activate)
    app.connect("shutdown", on_shutdown)

    
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
        app.quit()