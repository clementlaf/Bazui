from states.base_state import BaseState
from ui.widget import Widget
from ui.link import LinkByMethod

class TreeEditor(BaseState):
    def __init__(self, app):
        super().__init__(app)

        top_right_pos_link = LinkByMethod(self.app_state, lambda x: (x.screen_size[0] - 300, 0))
        self.ui_context.add_widget(Widget(top_right_pos_link, (300, 50), on_click=self.app.quit, background_color=(255, 0, 0)))
