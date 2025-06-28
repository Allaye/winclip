# gui/components/clip_card.py

from gi.repository import Gtk, Gio, Pango



class ClipCard(Gtk.Box):
    def __init__(self, content: str, pinned=False):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self.set_margin_top(6)
        self.set_margin_bottom(6)
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_hexpand(True)
        self.set_vexpand(False)
        self.set_css_classes(["clip-card"])
        self.set_size_request(-1, 80)  # -1 means keep default width; 80px height


        # --- Content label
        self.label = Gtk.Label(
            label=content,
            xalign=0,
            wrap=True,
            wrap_mode=Pango.WrapMode.WORD_CHAR,
            max_width_chars=50
        )
        self.label.set_hexpand(True)

        # --- Pin button (icon only)
        self.pin_button = Gtk.Button()
        icon_name = "emblem-favorite-symbolic" if pinned else "emblem-symbolic"
        self.pin_button.set_icon_name(icon_name)
        self.pin_button.set_valign(Gtk.Align.CENTER)
        self.pin_button.set_tooltip_text("Pin this clip")

        # --- Menu button (3 dots)
        self.menu_button = Gtk.MenuButton(icon_name="open-menu-symbolic")
        self.menu_button.set_valign(Gtk.Align.CENTER)

        # For now: dummy empty menu
        popover = Gtk.Popover()
        popover.set_child(Gtk.Label(label="More options..."))
        self.menu_button.set_popover(popover)

        # --- Pack widgets
        self.append(self.label)
        self.append(self.pin_button)
        self.append(self.menu_button)
