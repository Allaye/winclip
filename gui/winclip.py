# gui/window.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk # type: ignore  # noqa: E402

# Assuming widgets.clip_card.ClipCard is correctly defined
# from widgets.clip_card import ClipCard  # noqa: E402
from gui import ClipCard # noqa: E402
# Assuming widgets.header_bar.HeaderBar is your custom header bar for INSIDE the window
from gui import HeaderBar # noqa: E402
from gui.widgets.category_bar import CategoryBar

class ClipboardWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Configure window titlebar
        window_header_bar = Gtk.HeaderBar()
        window_header_bar.set_show_title_buttons(True)

        # Create smaller title label aligned to the left
        window_title_label = Gtk.Label(label="WinClip 🪟")
        window_title_label.set_css_classes(["title-small"])
        window_title_label.set_halign(Gtk.Align.START)
        
        # Pack the label to the start (left) of the header bar
        window_header_bar.pack_start(window_title_label) 
        
        # Set the header bar as the window's titlebar
        self.set_titlebar(window_header_bar)

        # --- Window Properties ---
        self.set_default_size(450, 540)
        self.set_margin_top(0)
        self.set_margin_bottom(0)
        self.set_margin_start(0)
        self.set_margin_end(0)
        self.set_resizable(False)
        self.set_deletable(True)
        # self.set_hide_on_close(True) # If you want to hide instead of close
        # self.set_titlebar(None) # This removes the titlebar entirely, commented out as you want one.

        # --- Main Layout for Window Content ---
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        
        # --- Category Icons Bar ---
        category_bar = CategoryBar()
        outer.append(category_bar)
        
        # --- Custom Header for Inner Content (your widgets.header_bar.HeaderBar) ---
        # This is the "Clipboard" label + "Clear all" button row you showed in the screenshot.
        # Ensure that in widgets/header_bar.py, your custom HeaderBar uses:
        # self.title_label.set_halign(Gtk.Align.START)
        # self.title_label.set_hexpand(True)
        inner_content_header = HeaderBar(on_clear_all=self.clear_all_clips)
        outer.append(inner_content_header)

        # --- Scrollable List of Clips ---
        self.clip_list = Gtk.ListBox()
        scroll = Gtk.ScrolledWindow()
        scroll.set_child(self.clip_list)
        scroll.set_vexpand(True) # Make it take full height
        outer.append(scroll)

        # --- Set Window Child and Load Data ---
        self.set_child(outer)
        # self.load_fake_data()
        self.refresh_clips()

    def create_display_content(self, original_content):
        """
        Create a display version of content that preserves structure but fits in the UI.
        This method creates a preview that maintains formatting while being display-friendly.
        """
        if not original_content:
            return ""
        
        # Split content into lines
        lines = original_content.split('\n')
        
        # Take first 3 lines for display
        display_lines = lines[:3]
        
        # Join lines back together, preserving line breaks
        display_content = '\n'.join(display_lines)
        
        # If we have more lines, add an indicator
        if len(lines) > 3:
            display_content += '\n...'
        
        # If content is still too long, truncate the last line
        if len(display_content) > 200:
            # Find the last complete word within 200 characters
            truncated = display_content[:200]
            last_space = truncated.rfind(' ')
            if last_space > 150:  # Only truncate if we can find a good break point
                display_content = truncated[:last_space] + '...'
            else:
                display_content = truncated + '...'
        
        return display_content

    # def load_fake_data(self):
    #     for i in range(5):
    #         # Pass False for Item 1 to match the screenshot where Item 1 is unpinned
    #         # and Item 2 and 3 are pinned (assuming green lock means pinned, red unpinned)
    #         card = ClipCard(content=f"Item {i+1}", pinned=(i == 1 or i == 2)) # Item 2 and 3 pinned
    #         self.clip_list.append(card)

    def clear_all_clips(self):
        print("Clear All clicked!")
        
        # Clear list box - GTK4 way
        while True:
            first_child = self.clip_list.get_first_child()
            if first_child is None:
                break
            self.clip_list.remove(first_child)
        self.refresh_clips()

    def refresh_clips(self):
        from engine.storage import get_recent_clips

        # Clear current list - GTK4 way
        while True:
            first_child = self.clip_list.get_first_child()
            if first_child is None:
                break
            self.clip_list.remove(first_child)

        # Load from DB
        clips = get_recent_clips(15)
        
        if not clips:
            # Show a message when no clips are available
            no_clips_label = Gtk.Label(label="No clipboard items yet.\nCopy something to get started!")
            no_clips_label.set_css_classes(["no-clips-message"])
            no_clips_label.set_halign(Gtk.Align.CENTER)
            no_clips_label.set_valign(Gtk.Align.CENTER)
            no_clips_label.set_vexpand(True)
            self.clip_list.append(no_clips_label)
        else:
            for clip in clips:
                # Only show clips with actual content
                if clip.content and clip.content.strip():
                    # Create a display version that preserves structure but limits length
                    display_content = self.create_display_content(clip.content)
                    
                    card = ClipCard(content=display_content, pinned=clip.pinned, original_content=clip.content)
                    self.clip_list.append(card)



