"""GTK4 application setup and lifecycle management for WinClip."""

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # type: ignore[import-untyped]
from gi.repository import GLib # type: ignore[import-untyped]
from engine.monitor import ClipboardMonitor
from engine.storage import insert_clip
from engine.model import Clip
from app.winclip import ClipboardWindow
from gui.styles import style


def update_ui(text, win):
    """Store a new clip and refresh the window.

    Args:
        text: The clipboard text to store.
        win: The ClipboardWindow instance, or None.

    Returns:
        False to remove the GLib idle source.
    """
    clip = Clip(content=text)
    insert_clip(clip)

    if win:
        win.refresh_clips()

    return False


def start_app(hide_gui=False):
    """Start the WinClip GTK application.

    Args:
        hide_gui: If True, start in background daemon mode without
            presenting the window.

    Returns:
        The Gtk.Application instance, or None on failure.
    """
    app = Gtk.Application(application_id="com.allaye.winclip")

    def on_activate(app):
        """Create or present the main window."""
        if app.hide_gui:
            app.hide_gui = False
            return

        if app.win is None:
            app.win = ClipboardWindow(application=app)

        app.win.present()

    def on_startup(app):
        """Initialise app state, load CSS, and start the clipboard monitor."""
        app.win = None
        app.monitor = None
        app.hide_gui = hide_gui
        style.load_css(app)

        # Keep the main loop alive even when no window is visible (daemon mode).
        app.hold()

        def on_clipboard_change(text):
            GLib.idle_add(update_ui, text, app.win)

        app.monitor = ClipboardMonitor(on_clipboard_change=on_clipboard_change)
        app.monitor.start()

    def on_shutdown(app):
        """Stop the clipboard monitor on exit."""
        if app.monitor is not None:
            app.monitor.stop()

    app.connect("startup", on_startup)
    app.connect("activate", on_activate)
    app.connect("shutdown", on_shutdown)

    app.run(None)
    return app