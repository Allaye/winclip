
import gi
import os
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

def load_css():
    provider = Gtk.CssProvider()
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, "style.css")
    provider.load_from_path(css_path)
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER
    )
