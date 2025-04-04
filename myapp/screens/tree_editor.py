from myapp.screens.app_base_state import AppBaseState
from ui.text import SingleLineText

class TreeEditor(AppBaseState):
    def __init__(self, app):
        super().__init__(app)

        self.title = "Tree Editor"

        self.ui_context.add_widget(SingleLineText((100, 100), (300, 50), "text", self.app, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu.", font=self.app_state.title1f, background_color=(255, 0, 255), size_auto_fit=True, can_be_selected=True, editable=False))
