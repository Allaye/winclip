# gui/window.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from widgets.clip_card import ClipCard
from widgets.header_bar import HeaderBar

class ClipboardWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Clipboard")
        self.set_default_size(400, 500)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_resizable(False)
        self.set_titlebar(None)
        self.set_resizable(False)
        self.set_deletable(True)
    # self.set_hide_on_close(True)
    # self.set_default_size(420, 520)
    # self.set_resizable(False)
    # self.set_title("Clipboard")

    # # Disable window buttons (min/max)
    # self.set_decorated(True)
    # self.set_type_hint(Gtk.WindowTypeHint.DIALOG)



        # Main layout
        outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        # outer.set_margin_top(12)
        # outer.set_margin_bottom(12)

        # Header with clear callback
        header = HeaderBar(on_clear_all=self.clear_all_clips)
        outer.append(header)

        # Scrollable list of clips
        self.clip_list = Gtk.ListBox()
        scroll = Gtk.ScrolledWindow()
        scroll.set_child(self.clip_list)

        # ✅ Make it take full height
        scroll.set_vexpand(True)
        outer.append(scroll)

        self.set_child(outer)
        self.load_fake_data()

    def load_fake_data(self):
        for i in range(3):
            card = ClipCard(content=f"Item {i+1}", pinned=(i == 1))
            self.clip_list.append(card)

    def clear_all_clips(self):
        print("Clear All clicked!")
        for row in self.clip_list.get_children():
            self.clip_list.remove(row)
