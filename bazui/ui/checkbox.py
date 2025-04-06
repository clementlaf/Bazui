from bazui.ui.widget import Widget

class CheckBox(Widget):
    def __init__(self, pos, size, name, app, **kwargs):
        super().__init__(pos, size, name, app)
        self.checked = False  # State of the checkbox (checked or unchecked)

        # Customizable attributes
        self.check_color = None  # Color of the check mark
        self.uncheck_color = None  # Color of the uncheck mark
        self.on_check = None
        self.on_uncheck = None

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"CheckBox has no attribute {key}")

        # forced attributes
        self.on_click = self._base_checkbox_click
        self.can_be_selected = True

        self._checkbox_setup()

    def _checkbox_setup(self):
        super()._widget_setup()

        if self.background_color is not None:
            if self.check_color is None:
                self.check_color = self.background_color
            if self.uncheck_color is None:
                self.uncheck_color = self.background_color

    def _base_checkbox_click(self, event):
        """Base method for checkbox click event."""
        self.checked = not self.checked
        if self.checked:
            if self.on_check:
                self.on_check(self)
        else:
            if self.on_uncheck:
                self.on_uncheck(self)

    def update(self):
        super().update()

        if self.checked:
            self.background_color = self.check_color
        else:
            self.background_color = self.uncheck_color
