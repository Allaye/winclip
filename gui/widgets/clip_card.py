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
        self.is_pinned = pinned
        # --- Pin button (icon only)
        self.pin_button = Gtk.Button()
        if pinned:
            icon_name = "object-locked-symbolic" # Or "locked-symbolic", "security-high-symbolic"
            tooltip_text = "Pinned. Click to unpin."
        else:
            icon_name = "object-unlocked-symbolic" # Or "unlocked-symbolic", "security-medium-symbolic"
            tooltip_text = "Not pinned. Click to pin."
        self.pin_button.set_icon_name(icon_name)
        self.pin_button.set_tooltip_text(tooltip_text)
        # icon_name = "pin-symbolic" if pinned else "pin-alt-symbolic"
        # self.pin_button.set_icon_name(icon_name)
        self.pin_button.set_valign(Gtk.Align.CENTER)
        # self.pin_button.set_tooltip_text("Pin this clip")

        # --- Menu button (3 dots)
        self.menu_button = Gtk.MenuButton(icon_name="open-menu-symbolic")
        self.menu_button.set_valign(Gtk.Align.CENTER)

        # For now: dummy empty menu
        # popover = Gtk.Popover()
        # popover.set_child(Gtk.Label(label="More options..."))
        # self.menu_button.set_popover(popover)

        # # --- Pack widgets
        # self.append(self.label)
        # self.append(self.pin_button)
        # self.append(self.menu_button)

        # --- Button column (Menu on top, Pin below)
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        button_box.set_valign(Gtk.Align.CENTER)
        button_box.append(self.menu_button)
        button_box.append(self.pin_button)

        # --- Pack main layout: label on left, button box on right
        self.append(self.label)
        self.append(button_box)

        #  connect action signals
        self.pin_button.connect("clicked", self.toggle_pin)





    def toggle_pin(self, button):
        self.is_pinned = not self.is_pinned

        icon_name = "object-locked-symbolic" if self.is_pinned else "object-unlocked-symbolic"
        tooltip = "Pinned. Click to unpin." if self.is_pinned else "Not pinned. Click to pin."

        self.pin_button.set_icon_name(icon_name)
        self.pin_button.set_tooltip_text(tooltip)

        print(f"[Pin] Toggled: {self.is_pinned}")

