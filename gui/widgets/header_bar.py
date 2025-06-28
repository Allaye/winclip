# gui/view/header_bar.py
import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

class HeaderBar(Gtk.Box):
    def __init__(self, on_clear_all):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_margin_top(12)
        self.set_margin_bottom(6)
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_spacing(8)
        self.set_hexpand(True)
        self.set_css_classes(["header-bar"])

        # Title label
        title_label = Gtk.Label(label="Clipboard")
        title_label.set_halign(Gtk.Align.START)
        title_label.set_valign(Gtk.Align.CENTER)
        title_label.set_css_classes(["header-title"])
        title_label.set_hexpand(True)

        # Clear All Button
        clear_button = Gtk.Button(label="Clear all")
        clear_button.set_valign(Gtk.Align.CENTER)
        clear_button.set_css_classes(["clear-button"])
        clear_button.connect("clicked", lambda btn: on_clear_all())

        # Add to layout
        self.append(title_label)
        self.append(clear_button)
