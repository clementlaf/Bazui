from states.base_state import BaseState
from ui.link import LinkByMethod
from myapp.UI_elements import state_selector_top_bar

class AppBaseState(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.setup_top_bar()

    def on_activation(self):

        # Update the top-bar
        self.setup_top_bar()

    def setup_top_bar(self):
        # Set up the top bar with the current state name
        self.ui_context.remove_widget(self.ui_context.getbywidget(self.ui_context["top_bar"])) # removes it if it already exists
        self.ui_context.add_widget(state_selector_top_bar.build(LinkByMethod(self.app_state, lambda x: x.screen_size), self.app, self.app_state.title1f))
