from myapp.screens.app_base_state import AppBaseState
from ui.text import SingleLineText
from ui.image import Image

class DebugWindow(AppBaseState):
    def __init__(self, app):
        super().__init__(app)

        self.title = "Debug"

        self.ui_context.add_widget(SingleLineText((100, 100), (300, 50), "text", self.app, text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu.", font=self.app_state.title1f, background_color=(255, 0, 255), size_auto_fit=True, can_be_selected=True, editable=False))

        self.ui_context.add_widget(SingleLineText((100, 200),
                                                  (300, 50),
                                                  "editable",
                                                  self.app,
                                                  text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed eu.",
                                                  font=self.app_state.title1f,
                                                  size_auto_fit=True,
                                                  can_be_selected=True,
                                                  editable=True,
                                                  contour_color="white",
                                                  contour_width=1,))

        self.ui_context.add_widget(Image((100, 300),
                                         (300, 300),
                                         "image",
                                         self.app,
                                         image=self.app_state.test_image,
                                         im_sizing="stretch", 
                                         contour_color="white",
                                         contour_width=1,
                                         corner_radius=10,))
