class UIContext:
    """Manages UI components and layout."""
    def __init__(self, app_state):
        self.app_state = app_state
        self.widgets = {}  # Store UI elements like buttons, panels, etc.
        self.sorted_widgets = []
        self.crt_max_id = 0
        self.exit_events = False  # Flag to indicate if the update loop should exit

    def add_widget(self, widget):
        """Add a widget to the UI context."""
        free_id = self.crt_max_id
        self.widgets[free_id] = widget
        self.sorted_widgets = sorted(self.widgets.values(), key=lambda x: x.z, reverse=True)
        self.crt_max_id += 1
        return widget

    def handle_events(self, event):
        self.exit_events = False  # Reset exit flag for each event
        for widget in self.sorted_widgets:
            res = widget.handle_event(event)
            if self.exit_events or res:
                # If the widget consumed the event or if we are exiting, break the loop
                return res
        return False

    def update(self):
        for widget in self.sorted_widgets:
            widget.update()

    def draw(self, screen):
        for widget in self.sorted_widgets[::-1]:
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
        try:
            del self.widgets[widget_id]
            self.sorted_widgets = sorted(self.widgets.values(), key=lambda x: x.z, reverse=True)
        except KeyError:
            # the widget was not found
            pass
        except Exception as e:
            print(f"Error removing widget: {e}")

    def __repr__(self):
        txt = []
        for widget_id, widget in self.widgets.items():
            txt.append(f"{widget_id}: {widget}")
        return "\n".join(txt)

    def recursive_widget_list(self):
        """Recursively get all widgets in the context."""
        widget_list = []
        for widget in self.widgets.values():
            if hasattr(widget, 'childs'):
                widget_list.extend(widget.recursive_widget_list())
            else:
                widget_list.append(widget)
        return widget_list
