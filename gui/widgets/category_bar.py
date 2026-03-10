# gui/widgets/category_bar.py
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class CategoryBar(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.set_margin_top(4)
        self.set_margin_bottom(4)
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_spacing(12)
        self.set_halign(Gtk.Align.START)
        self.set_css_classes(["category-bar"])
        
        # Create category icons
        categories = [
            ("heart", "♡", "Favorites"),
            ("face-smile", "☹︎", "Emojis"),
            ("image", "🖼️", "Images"),
            ("face-wink", ";-)", "Expressions"),
            ("percent", "% A+", "Grades"),
            ("edit-copy", "📋", "Clipboard")
        ]
        
        for icon_name, symbol, tooltip in categories:
            button = Gtk.Button()
            button.set_css_classes(["category-button"])
            button.set_tooltip_text(tooltip)
            
            # Use symbol for now, can be replaced with proper icons later
            label = Gtk.Label(label=symbol)
            label.set_css_classes(["category-icon"])
            button.set_child(label)
            
            # Make clipboard icon active by default
            if icon_name == "edit-copy":
                button.set_css_classes(["category-button", "category-button-active"])
            
            button.connect("clicked", self.on_category_clicked, icon_name)
            self.append(button)
    
    def on_category_clicked(self, button, category):
        # Remove active class from all buttons
        for child in self:
            if isinstance(child, Gtk.Button):
                child.set_css_classes(["category-button"])
        
        # Add active class to clicked button
        button.set_css_classes(["category-button", "category-button-active"])
        
        print(f"Category clicked: {category}")
        # TODO: Implement category filtering
