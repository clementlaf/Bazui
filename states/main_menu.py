import pygame
from states.base_state import BaseState
from states.event_helpers import consume_event
from ui.widget import Widget
from ui.grid import Grid
from ui.link import LinkAttribute, LinkByMethod

import math
import time

class MainMenu(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.font = pygame.font.Font(None, 50)

        self.ui_context.add_widget(Widget((100, 400), (200, 50), on_click=self.app.quit, background_color=(255, 0, 0)))
        test_grid = self.ui_context.add_widget(Grid((100, 0), (200, 200), (2, 2),
                                                     background_color=(0, 255, 0),
                                                     on_click=self.app.quit,
                                                     padding=10,
                                                     margin=20,
                                                     has_surface=True))
        cell_size_link = LinkAttribute(self.ui_context.get(test_grid), "cell_size")
        self.ui_context.get(test_grid).set_child((0, 0), Widget(None, cell_size_link))
        self.ui_context.get(test_grid).set_child((1, 0), Widget(None, cell_size_link, background_color=(0, 0, 255), on_click=consume_event))
        self.ui_context.get(test_grid).set_child((0, 1), Widget(None, cell_size_link, background_color=(255, 0, 255), on_click=lambda: print("Clicked")))
        self.ui_context.get(test_grid).set_child((1, 1), Widget(None, cell_size_link, background_color=(255, 255, 0)))

        bottom_bar_pos_link = LinkByMethod(self.app_state, lambda x: (0, x.screen_size[1] - 50))
        bottom_bar_size_link = LinkByMethod(self.app_state, lambda x: (x.screen_size[0], 50))
        self.ui_context.add_widget(Widget(bottom_bar_pos_link, bottom_bar_size_link, background_color=(0, 255, 255), on_click=self.app.quit))

    def to_tree_editor(self):
        from states.tree_editor import TreeEditor
        self.app.state_manager.change_state(TreeEditor(self.app))

    def to_timeline_editor(self):
        from states.timeline_editor import TimelineEditor
        self.app.state_manager.change_state(TimelineEditor(self.app))

    def to_character_sheets(self):
        from states.character_sheet import CharacterSheet
        self.app.state_manager.change_state(CharacterSheet(self.app))
