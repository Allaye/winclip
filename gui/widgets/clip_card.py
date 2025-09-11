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
        self.set_size_request(-1, 70)  # Fixed height of 70px
        
        # Create a fixed-size container for the content
        content_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        content_container.set_size_request(-1, 70)
        content_container.set_vexpand(False)


        # --- Content label with improved text structure
        self.label = Gtk.Label(
            label=content,
            xalign=0,  # Align text to the left
            yalign=0,  # Align text to the top
            wrap=True,  # Enable wrapping so text breaks to next line
            wrap_mode=Pango.WrapMode.WORD_CHAR,  # Wrap at word boundaries or characters
            ellipsize=Pango.EllipsizeMode.END,  # Show ellipsis for long content
            max_width_chars=50,  # Further reduced width
            selectable=True,  # Make text selectable
            lines=2  # Limit to 2 lines to fit in 70px height
        )
        self.label.set_hexpand(True)
        self.label.set_vexpand(False)
        self.label.set_halign(Gtk.Align.START)  # Align label to start (left)
        self.label.set_valign(Gtk.Align.START)  # Align label to start (top)
        self.label.set_css_classes(["clip-content"])
        self.label.set_size_request(-1, 50)  # Constrain label height
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
        self.paste_button.set_tooltip_text("Paste at cursor (requires ydotool)")
        self.paste_button.connect("clicked", self.paste_to_clipboard)

        # # --- Pack widgets
        # self.append(self.label)
        # self.append(self.pin_button)
        # self.append(self.menu_button)

        # --- Button column (Paste on top, Pin below)
        button_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        button_box.set_valign(Gtk.Align.START)  # Align buttons to top instead of center
        button_box.set_margin_start(8)  # Add some space between content and buttons
        button_box.set_size_request(-1, 50)  # Constrain button box height
        button_box.append(self.paste_button)
        button_box.append(self.pin_button)

        # --- Pack content container: label on left, button box on right
        content_container.append(self.label)
        content_container.append(button_box)
        
        # --- Pack main layout: content container
        self.append(content_container)

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
        import time
        
        try:
            # Method 1: Try ydotool type (direct typing at cursor)
            try:
                result = subprocess.run(['ydotool', 'type', self.original_content], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return  # Success - content typed at cursor
                else:
                    pass  # Continue to next method
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                pass  # Continue to next method
            
            # Method 2: Try xdotool type (legacy direct typing)
            try:
                result = subprocess.run(['xdotool', 'type', self.original_content], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return  # Success - content typed at cursor
                else:
                    pass  # Continue to next method
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                pass  # Continue to next method
            
            # Method 3: Copy to clipboard + simulate Ctrl+V (paste at cursor)
            try:
                # Copy content to clipboard
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                process.communicate(input=self.original_content.encode('utf-8'))
                
                # Small delay to ensure clipboard is updated
                time.sleep(0.1)
                
                # Try to simulate Ctrl+V with ydotool (this pastes at cursor)
                try:
                    result = subprocess.run(['ydotool', 'key', 'ctrl+v'], 
                                          capture_output=True, text=True, timeout=3)
                    if result.returncode == 0:
                        return  # Success - content pasted at cursor
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    pass
                
                # Try xdotool Ctrl+V (this pastes at cursor)
                try:
                    result = subprocess.run(['xdotool', 'key', 'ctrl+v'], 
                                          capture_output=True, text=True, timeout=3)
                    if result.returncode == 0:
                        return  # Success - content pasted at cursor
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    pass
                
            except Exception:
                pass  # Continue to fallback
            
            # Method 4: Fallback - copy to clipboard (user must press Ctrl+V)
            try:
                # Copy content to clipboard
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                process.communicate(input=self.original_content.encode('utf-8'))
                # Content is now in clipboard - user can press Ctrl+V to paste at cursor
            except Exception:
                pass  # Silent failure
            
        except Exception:
            pass  # Silent failure




