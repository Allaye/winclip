# gui/window.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

# Assuming widgets.clip_card.ClipCard is correctly defined
from widgets.clip_card import ClipCard
# Assuming widgets.header_bar.HeaderBar is your custom header bar for INSIDE the window
from widgets.header_bar import HeaderBar 

class ClipboardWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # --- Configure the Window's Official Titlebar (Gtk.HeaderBar) ---
        # Create the standard Gtk.HeaderBar for the window's top title area
        window_header_bar = Gtk.HeaderBar()
        window_header_bar.set_show_title_buttons(True) # Keep min/max/close buttons

        # Create the label for the window's title
        window_title_label = Gtk.Label(label="Clipboard and more - WinClip 🪟")
        
        # Pack the label to the start (left) of the window's header bar
        window_header_bar.pack_start(window_title_label) 
        
        # Set this configured Gtk.HeaderBar as the window's title bar
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
        self.load_fake_data()

    def load_fake_data(self):
        for i in range(5):
            # Pass False for Item 1 to match the screenshot where Item 1 is unpinned
            # and Item 2 and 3 are pinned (assuming green lock means pinned, red unpinned)
            card = ClipCard(content=f"Item {i+1}", pinned=(i == 1 or i == 2)) # Item 2 and Item 3 pinned
            self.clip_list.append(card)

    def clear_all_clips(self):
        print("Clear All clicked!")
        
        for row in self.clip_list.get_children():
            self.clip_list.remove(row)