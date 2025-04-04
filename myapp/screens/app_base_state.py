from states.base_state import BaseState
from myapp.UI_elements import state_selector_top_bar

class AppBaseState(BaseState):

    def __init__(self, app):
        super().__init__(app)

        self.title = "App Base State"

    def on_activation(self):

        # Update the top-bar
        self.setup_top_bar()

    def setup_top_bar(self):
        # Set up the top bar with the current state name
        self.ui_context.remove_widget(self.ui_context.getbywidget(self.ui_context["top_bar"])) # removes it if it already exists
        self.ui_context.add_widget(state_selector_top_bar.build(self.app, self.app_state.title1f, self.close_window))

    def close_window(self, widget):
        """Close the current window and remove it from the state manager."""
        self.app.state_manager.close_crt_state()
