# gui/components/clip_card.py

from gi.repository import Gtk, Gio, Pango



class ClipCard(Gtk.Box):
    def __init__(self, content: str, pinned=False, original_content=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.set_margin_top(4)
        self.set_margin_bottom(4)
        self.set_margin_start(16)
        self.set_margin_end(16)
        self.set_hexpand(True)
        self.set_vexpand(False)
        self.set_css_classes(["clip-card"])
        self.set_size_request(-1, -1)  # Allow dynamic height based on content


        # --- Content label with improved text structure
        self.label = Gtk.Label(
            label=content,
            xalign=0,  # Align text to the left
            yalign=0,  # Align text to the top
            wrap=True,  # Enable wrapping so text breaks to next line
            wrap_mode=Pango.WrapMode.WORD_CHAR,  # Wrap at word boundaries or characters
            ellipsize=Pango.EllipsizeMode.END,  # Show ellipsis for long content
            max_width_chars=75,  # Optimized width for better readability
            selectable=True,  # Make text selectable
            lines=3  # Allow 3 lines for better content display
        )
        self.label.set_hexpand(True)
        self.label.set_vexpand(False)
        self.label.set_halign(Gtk.Align.START)  # Align label to start (left)
        self.label.set_valign(Gtk.Align.START)  # Align label to start (top)
        self.label.set_css_classes(["clip-content"])
        self.is_pinned = pinned
        self.original_content = original_content or content
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

        # --- Paste button
        self.paste_button = Gtk.Button(icon_name="edit-paste-symbolic")
        self.paste_button.set_valign(Gtk.Align.CENTER)
        self.paste_button.set_tooltip_text("Paste directly at cursor location")
        self.paste_button.connect("clicked", self.paste_to_clipboard)

        # # --- Pack widgets
        # self.append(self.label)
        # self.append(self.pin_button)
        # self.append(self.menu_button)

        # --- Button column (Paste on top, Pin below)
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        button_box.set_valign(Gtk.Align.START)  # Align buttons to top instead of center
        button_box.set_margin_start(8)  # Add some space between content and buttons
        button_box.append(self.paste_button)
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

    def paste_to_clipboard(self, button):
        """Paste content directly at cursor location"""
        import subprocess
        
        try:
            # Use xdotool to type the content directly at cursor location
            subprocess.run(['xdotool', 'type', self.original_content], check=True)
            print(f"[Paste] Successfully pasted at cursor: {self.original_content[:50]}...")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # xdotool not available or failed
            print(f"[Info] xdotool not available - install it for direct pasting")
            print(f"[Info] Command: sudo apt install xdotool")
            
        except Exception as e:
            print(f"[Error] Failed to paste at cursor: {e}")




