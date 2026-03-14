"""Clipboard entry card widget with copy, paste, and pin controls."""

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib, Pango


class ClipCard(Gtk.Box):
    """A card displaying a single clipboard entry with action buttons."""

    def __init__(self, content: str, pinned=False, original_content=None, clip_id=None):
        """Create a clip card.

        Args:
            content: Truncated display text for the label.
            pinned: Whether the clip is currently pinned.
            original_content: Full clipboard text (defaults to *content*).
            clip_id: Database UUID of the clip.
        """
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.set_margin_top(4)
        self.set_margin_bottom(4)
        self.set_margin_start(16)
        self.set_margin_end(16)
        self.set_hexpand(True)
        self.set_vexpand(False)
        self.set_css_classes(["clip-card"])

        # --- Config
        FIXED_HEIGHT = 70
        self.set_size_request(-1, FIXED_HEIGHT)

        # --- Store content
        self.content = content
        self.is_pinned = pinned
        self.original_content = original_content or content
        self.clip_id = clip_id

        # --- Content container (fixed height)
        content_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        content_container.set_vexpand(False)
        content_container.set_valign(Gtk.Align.FILL)
        content_container.set_size_request(-1, FIXED_HEIGHT)

        # --- Label
        self.label = Gtk.Label(
            label=content,
            xalign=0,
            yalign=0,
            wrap=True,
            wrap_mode=Pango.WrapMode.WORD_CHAR,
            ellipsize=Pango.EllipsizeMode.END,
            max_width_chars=50,
            selectable=True,
        )
        self.label.set_hexpand(True)
        self.label.set_vexpand(False)
        self.label.set_valign(Gtk.Align.FILL)
        self.label.set_halign(Gtk.Align.FILL)
        self.label.set_css_classes(["clip-content"])
        self.label.set_size_request(-1, FIXED_HEIGHT - 20)

        # --- Buttons
        self.pin_button = Gtk.Button(icon_name="object-locked-symbolic" if pinned else "object-unlocked-symbolic")
        self.pin_button.set_tooltip_text("Pinned. Click to unpin." if pinned else "Click to pin.")
        self.pin_button.set_valign(Gtk.Align.CENTER)
        self.pin_button.connect("clicked", self.on_pin_clicked)

        self.paste_button = Gtk.Button(icon_name="edit-paste-symbolic")
        self.paste_button.set_valign(Gtk.Align.CENTER)
        self.paste_button.set_tooltip_text("Copy and paste automatically")
        self.paste_button.connect("clicked", self.paste_to_cursor)

        # --- Button column
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        button_box.set_vexpand(False)
        button_box.set_valign(Gtk.Align.CENTER)
        button_box.set_size_request(-1, FIXED_HEIGHT - 20)
        button_box.append(self.paste_button)
        button_box.append(self.pin_button)

        # --- Pack
        content_container.append(self.label)
        content_container.append(button_box)
        self.append(content_container)

    def _copy_to_system_clipboard(self):
        """Copy ``original_content`` to the system clipboard.

        Uses ``wl-copy`` on Wayland (with ``xclip`` fallback for XWayland
        apps) and falls back to the GDK4 clipboard.

        Returns:
            True if the copy succeeded, False otherwise.
        """
        import subprocess
        import shutil
        import os

        text = self.original_content
        session_type = os.environ.get("XDG_SESSION_TYPE", "x11")

        if session_type == "wayland" and shutil.which("wl-copy"):
            try:
                subprocess.Popen(
                    ["wl-copy"],
                    stdin=subprocess.PIPE,
                ).communicate(input=text.encode(), timeout=2)
                if shutil.which("xclip"):
                    subprocess.Popen(
                        ["xclip", "-selection", "clipboard"],
                        stdin=subprocess.PIPE,
                    ).communicate(input=text.encode(), timeout=2)
                return True
            except Exception:
                pass

        # Last resort: GDK4 clipboard (may not persist after focus loss on Wayland)
        display = Gdk.Display.get_default()
        if display:
            clipboard = display.get_clipboard()
            clipboard.set(text)
            return True

        return False

    def _simulate_paste(self):
        """Simulate a Ctrl+V keystroke via ``ydotool`` or ``xdotool``.

        Returns:
            False to remove the GLib timeout source.
        """
        import subprocess
        import shutil
        import os

        session_type = os.environ.get("XDG_SESSION_TYPE", "x11")

        if session_type == "wayland" and shutil.which("ydotool"):
            subprocess.Popen(
                ["ydotool", "key", "ctrl+v"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif shutil.which("xdotool"):
            subprocess.Popen(["xdotool", "key", "ctrl+v"])
        return False

    def _show_toast(self, message):
        """Show a brief toast notification on the parent window.

        Args:
            message: The text to display.
        """
        window = self.get_root()
        if isinstance(window, Gtk.ApplicationWindow):
            pass

    def paste_to_cursor(self, _button):
        """Copy content to clipboard, minimise the window, and simulate paste.

        Args:
            _button: The clicked button widget (unused).
        """
        if not self._copy_to_system_clipboard():
            return
        window = self.get_root()
        if isinstance(window, Gtk.Window):
            window.minimize()
            GLib.timeout_add(800, self._simulate_paste)  # simulate paste after a short delay
        

    def on_pin_clicked(self, _button):
        """Toggle the pinned state and persist to the database.

        Args:
            _button: The clicked button widget (unused).
        """
        self.is_pinned = not self.is_pinned
        self.pin_button.set_icon_name(
            "object-locked-symbolic" if self.is_pinned else "object-unlocked-symbolic"
        )
        self.pin_button.set_tooltip_text(
            "Pinned. Click to unpin." if self.is_pinned else "Click to pin."
        )
        # Persist to database
        if self.clip_id:
            from engine.storage import pin_unpin_clip
            from engine.model import Clip
            clip = Clip(id=self.clip_id, pinned=self.is_pinned)
            pin_unpin_clip(clip)


