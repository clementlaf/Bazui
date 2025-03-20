class UIContext:
    def __init__(self, app_state):
        self.app_state = app_state
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    def draw(self, screen):
        for widget in self.widgets:
            widget.draw(screen)
