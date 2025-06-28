# gui/app.py
import gi
from winclip import ClipboardWindow

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

def launch_gui():
    app = Gtk.Application(application_id="com.clipboard.manager10111")

    def on_activate(app):
        # Load CSS
        from styles import style
        style.load_css()

        win = ClipboardWindow(application=app)
        win.present()

    app.connect("activate", on_activate)
    app.run(None)
    try:
        app.run(None)
    except Exception as e:
        print("GTK app failed to run:", e)

if __name__ == "__main__":
    launch_gui()
    
