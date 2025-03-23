class UIContext:
    """Manages UI components and layout."""
    def __init__(self, app_state):
        self.app_state = app_state
        self.widgets = {}  # Store UI elements like buttons, panels, etc.
        self.crt_max_id = 0

    def add_widget(self, widget):
        """Add a widget to the UI context."""
        free_id = self.crt_max_id
        self.widgets[free_id] = widget
        self.crt_max_id += 1
        return free_id

    def handle_events(self, event):
        for widget in self.widgets.values():
            widget.handle_event(event)

    def update(self):
        for widget in self.widgets.values():
            widget.update()

    def draw(self, screen):
        for widget in self.widgets.values():
            widget.draw(screen)

    def getbyid(self, widget_id):
        return self.widgets.get(widget_id)
    def getbywidget(self, widget):
        for widget_id, stored_widget in self.widgets.items():
            if widget == stored_widget:
                return widget_id
    def __getitem__(self, widget_name):
        for widget in self.widgets.values():
            if widget.name == widget_name:
                return widget
        return None

    def remove_widget(self, widget_id):
        del self.widgets[widget_id]
