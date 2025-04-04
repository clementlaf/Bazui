import pygame
from states.base_state import BaseState
from states.event_helpers import consume_event, no_selection
from ui.widget import Widget
from ui.grid import Grid
from ui.text import SingleLineText
from ui.link import LinkAttribute, LinkByMethod

from myapp.UI_elements import state_selector_top_bar

class MainMenu(BaseState):
    def __init__(self, app):
        super().__init__(app)

        self.title1f = pygame.font.Font(self.app_state.text_font, 50)
        self.text1f = pygame.font.Font(self.app_state.text_font, 20)

        # Add the window selection bar
        screen_size_link = LinkByMethod(self.app_state, lambda x: x.screen_size)
        self.ui_context.add_widget(state_selector_top_bar.build(screen_size_link, self.app, self.title1f))

        # self.ui_context.add_widget(Widget((100, 400), (200, 50), "1", self.app, on_click=self.app.quit, background_color=(255, 0, 0)))
        # test_grid = self.ui_context.add_widget(Grid((100, 50), (200, 200), "test_grid", self.app, (2, 2),
        #                                                 background_color=(0, 255, 0),
        #                                                 on_click=self.app.quit,
        #                                                 padding=10,
        #                                                 margin=20,
        #                                                 has_surface=True))
        # cell_size_link = LinkAttribute(self.ui_context.getbyid(test_grid), "cell_size")
        # self.ui_context.getbyid(test_grid).set_child((0, 0), Widget(None, cell_size_link, "0", self.app))
        # self.ui_context.getbyid(test_grid).set_child((1, 0), Widget(None, cell_size_link, "1", self.app, background_color=(0, 0, 255), on_click=consume_event))
        # self.ui_context.getbyid(test_grid).set_child((0, 1), Widget(None, cell_size_link, "2", self.app, background_color=(255, 0, 255), on_click=lambda widget: print("Clicked")))
        # self.ui_context.getbyid(test_grid).set_child((1, 1), Widget(None, cell_size_link, "3", self.app, background_color=(255, 255, 0), can_be_selected=True))

        # bottom_bar_pos_link = LinkByMethod(self.app_state, lambda x: (0, x.screen_size[1] - 50))
        # bottom_bar_size_link = LinkByMethod(self.app_state, lambda x: (x.screen_size[0], 50))
        # bottom_bar = self.ui_context.add_widget(Widget(bottom_bar_pos_link, bottom_bar_size_link, "bottom_bar", self.app, background_color=(0, 255, 255), on_click=self.to_tree_editor))
        
        # text_pos_link = LinkAttribute(self.ui_context.getbyid(bottom_bar), "pos")
        # self.ui_context.getbyid(bottom_bar).set_child(SingleLineText(text_pos_link, (300, 100), "text", self.app, text="test", font=self.font, on_click=consume_event, background_color=(255, 0, 255), size_auto_fit=True, can_be_selected=True, editable=True))


        # add buttons for each available window
        available_windows = {
            "Tree Editor": self.add_tree_editor,
            "Debug Window": self.add_debug_window,
        }
        n = len(available_windows)

        grid_size = (200, (n+1)*20+n*40)
        grid_pos_link = LinkByMethod(self.app_state, lambda x: (x.screen_size[0]/2 - grid_size[0] / 2, 100))
        window_listing_grid = self.ui_context.add_widget(Grid(grid_pos_link, grid_size, "window_listing_grid", self.app, (1, n),
                                                background_color=(0, 255, 0),
                                                padding=10,
                                                margin=20,
                                                has_surface=True))
        cell_size_link = LinkAttribute(self.ui_context.getbyid(window_listing_grid), "cell_size")
        for i, (window_name, window_func) in enumerate(available_windows.items()):
            cell_pos = (0, i)
            button = self.ui_context.getbyid(window_listing_grid).set_child(cell_pos, Widget(None,
                                                                                            cell_size_link,
                                                                                            window_name,
                                                                                            self.app,
                                                                                            on_click=window_func,
                                                                                            background_color=(0, 0, 255)))
            text_pos_link = LinkAttribute(button, "pos")
            button.set_child(SingleLineText(text_pos_link,
                                            cell_size_link,
                                            f"{window_name}_text",
                                            self.app, text=window_name,
                                            font=self.text1f,
                                            size_auto_fit=False,
                                            text_color=(0, 0, 0),
                                            on_drag=no_selection))


    def add_tree_editor(self, widget):
        from myapp.screens.tree_editor import TreeEditor
        self.app.state_manager.add_state(TreeEditor(self.app))

    def add_debug_window(self, widget):
        from myapp.screens.debug_window import DebugWindow
        self.app.state_manager.add_state(DebugWindow(self.app))

    def update(self):
        self.ui_context.remove_widget(self.ui_context.getbywidget(self.ui_context["top_bar"]))
        self.ui_context.add_widget(state_selector_top_bar.build(LinkByMethod(self.app_state, lambda x: x.screen_size), self.app, self.title1f))
        super().update()
