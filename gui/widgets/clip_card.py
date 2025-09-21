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

        # --- Paste button (automatically pastes content)
        self.paste_button = Gtk.Button(icon_name="edit-paste-symbolic")
        self.paste_button.set_valign(Gtk.Align.CENTER)
        self.paste_button.set_tooltip_text("Copy and paste automatically")
        self.paste_button.connect("clicked", self.paste_to_clipboard)

        # # --- Pack widgets
        # self.append(self.label)
        # self.append(self.pin_button)
        # self.append(self.menu_button)

        # --- Button column (Auto-paste on top, Pin below)
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
        
        # TODO: Update pin status in database
        # This would require passing the clip ID to the ClipCard
        # and calling engine.storage.pin_unpin_clip()

    def paste_to_clipboard(self, button):
        """Copy content to clipboard and automatically paste it using python-uinput"""
        import subprocess
        import time
        import uinput
        
        try:
            # Copy content to system clipboard using xclip
            process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            process.communicate(input=self.original_content.encode('utf-8'))
            
            print(f"[Clipboard] Content copied: {self.original_content[:50]}...")
            
            # Minimize the WinClip window so it doesn't interfere with pasting
            try:
                # Get the window and minimize it
                window = button.get_root()
                if window:
                    window.minimize()
                    print("[Clipboard] WinClip window minimized")
            except:
                pass
            
            # Give user time to click on VS Code or any other application
            print("[Clipboard] Click on VS Code (or any app) where you want to paste, then wait...")
            time.sleep(2.0)  # Give user 2 seconds to click on target app
            
            # Automatically paste using python-uinput
            try:
                # Create virtual keyboard device
                device = uinput.Device([
                    uinput.KEY_LEFTCTRL,
                    uinput.KEY_V,
                ])
                
                # Simulate Ctrl+V
                device.emit_combo([
                    uinput.KEY_LEFTCTRL,
                    uinput.KEY_V,
                ])
                
                # Clean up
                device.destroy()
                
                print("[Clipboard] Content automatically pasted!")
                
            except Exception as e:
                print(f"[Clipboard] Auto-paste failed: {e}")
                print("[Clipboard] Content is in clipboard - press Ctrl+V to paste")
            
        except Exception as e:
            print(f"[Clipboard] Error: {e}")




