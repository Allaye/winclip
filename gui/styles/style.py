from gi.repository import Gtk, Gdk

def load_css():
    provider = Gtk.CssProvider()
    provider.load_from_path("./styles/style.css")
    Gtk.StyleContext.add_provider_for_display(
        Gdk.Display.get_default(),
        provider,
        Gtk.STYLE_PROVIDER_PRIORITY_USER
    )
