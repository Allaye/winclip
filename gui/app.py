# gui/app.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from .winclip import ClipboardWindow
from .styles import style

def launch_gui():
    app = Gtk.Application(application_id="com.allaye.winclip")

    window_holder = {}

    def on_activate(app):
        try:
            style.load_css()
            win = ClipboardWindow(application=app)
            win.present()
            window_holder["win"] = win
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
        return window_holder.get("win")
    except Exception as e:
        print(f"Failed to run application: {e}")
        import traceback
        traceback.print_exc()
        return None
