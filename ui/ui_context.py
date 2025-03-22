class UIContext:
    """Manages UI components and layout."""
    def __init__(self, app_state):
        self.app_state = app_state
        self.widgets = []  # Store UI elements like buttons, panels, etc.

    def add_widget(self, widget):
        self.widgets.append(widget)

    def handle_events(self, event):
        for widget in self.widgets:
            widget.handle_event(event)

    def draw(self, screen):
        for widget in self.widgets:
            widget.draw(screen)
