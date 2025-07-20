# gui/window.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk # type: ignore  # noqa: E402

# Assuming widgets.clip_card.ClipCard is correctly defined
# from widgets.clip_card import ClipCard  # noqa: E402
from gui import ClipCard # noqa: E402
# Assuming widgets.header_bar.HeaderBar is your custom header bar for INSIDE the window
from gui import HeaderBar # noqa: E402

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
        self.set_default_size(400, 500)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_resizable(False) # Redundant, you set it twice. Keep one.
        self.set_deletable(True)
        # self.set_hide_on_close(True) # If you want to hide instead of close
        # self.set_titlebar(None) # This removes the titlebar entirely, commented out as you want one.

        # --- Main Layout for Window Content ---
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        
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

    # def load_fake_data(self):
    #     for i in range(5):
    #         # Pass False for Item 1 to match the screenshot where Item 1 is unpinned
    #         # and Item 2 and 3 are pinned (assuming green lock means pinned, red unpinned)
    #         card = ClipCard(content=f"Item {i+1}", pinned=(i == 1 or i == 2)) # Item 2 and Item 3 pinned
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
        for clip in get_recent_clips(15):
            # Limit content to exactly 150 characters (including spaces, emojis, etc.)
            display_content = clip.content
            if len(display_content) > 250:
                display_content = display_content[:250] + "..."

            # Replace newlines with spaces for compact display
            display_content = display_content.replace('\n', ' ').replace('\r', ' ')
            
            card = ClipCard(content=display_content, pinned=clip.pinned)
            self.clip_list.append(card)



