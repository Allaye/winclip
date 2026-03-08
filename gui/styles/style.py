
import gi
import os
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk


def load_css(app: Gtk.Application = None):
    provider = Gtk.CssProvider()
    
    # Get the correct path to the CSS file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_path = os.path.join(current_dir, "style.css")
    
    try:
        provider.load_from_path(css_path)
        print(f"[CSS] Loaded styles from: {css_path}")
    except Exception as e:
        print(f"[CSS] Failed to load styles: {e}")
        return

    # GTK4: Get the default display
    try:
        display = Gdk.Display.get_default()
        if display is not None:
            Gtk.StyleContext.add_provider_for_display(
                display,
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            print("[CSS] Styles applied successfully")
        else:
            print("Warning: No display found. CSS not applied.")
    except Exception as e:
        print(f"[CSS] Failed to apply styles: {e}")
