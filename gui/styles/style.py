"""Load and apply GTK4 CSS styles."""

import gi
import os
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk


def load_css(app: Gtk.Application = None):
    """Load the application CSS and apply it to the default display.

    Args:
        app: The Gtk.Application instance (unused, reserved for future use).
    """
    provider = Gtk.CssProvider()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, "style.css")

    provider.load_from_path(css_path)

    display = Gdk.Display.get_default()
    if display is not None:
        Gtk.StyleContext.add_provider_for_display(
            display,
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
