from myapp.screens.app_base_state import AppBaseState
from states.event_helpers import consume_event, no_selection
from ui.widget import Widget
from ui.grid import Grid
from ui.text import SingleLineText
from ui.link import LinkAttribute, LinkByMethod, get

class MainMenu(AppBaseState):
    def __init__(self, app):
        super().__init__(app)

        # add buttons for each available window
        available_windows = {
            "Tree Editor": self.add_tree_editor,
            "Debug Window": self.add_debug_window,
        }
        n = len(available_windows)

        grid_size = (200, (n+1)*10+n*20)
        grid_pos_link = LinkByMethod(self.app_state, lambda x: (x.screen_size[0]/2 - grid_size[0] / 2, 100))
        window_listing_grid = self.ui_context.add_widget(Grid(grid_pos_link, grid_size, "window_listing_grid", self.app, (1, n),
                                                background_color="#252526",
                                                padding=10,
                                                margin=10,
                                                has_surface=True,
                                                corner_radius=10,
                                                contour_color="white",
                                                contour_width=1))
        cell_size_link = LinkAttribute(self.ui_context.getbyid(window_listing_grid), "cell_size")
        for i, (window_name, window_func) in enumerate(available_windows.items()):
            cell_pos = (0, i)
            button = self.ui_context.getbyid(window_listing_grid).set_child(cell_pos, Widget(None,
                                                                                            cell_size_link,
                                                                                            window_name,
                                                                                            self.app,
                                                                                            on_click=window_func,))
            text_pos_link = LinkAttribute(button, "pos")
            text = button.set_child(SingleLineText(text_pos_link,
                                            cell_size_link,
                                            f"{window_name}_text",
                                            self.app, text=window_name,
                                            font=self.app_state.text1f,
                                            size_auto_fit=False,
                                            text_color="white",
                                            on_drag=no_selection))
            
            # add line over the button
            if i != 0:
                line_pos_link = LinkByMethod(text, lambda x: (get(x.pos)[0], get(x.pos)[1] - 5))
                line_size = grid_size[0] - 20, 1
                self.ui_context.add_widget(Widget(line_pos_link, line_size, f"{window_name}_line", self.app, background_color="#3C3C3D"))


    def add_tree_editor(self, widget):
        from myapp.screens.tree_editor import TreeEditor
        self.app.state_manager.add_state(TreeEditor(self.app))
        self.setup_top_bar()

    def add_debug_window(self, widget):
        from myapp.screens.debug_window import DebugWindow
        self.app.state_manager.add_state(DebugWindow(self.app))
        self.setup_top_bar()
