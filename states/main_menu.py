import pygame
from states.base_state import BaseState
from ui.button import Button

class MainMenu(BaseState):
    def __init__(self, app):
        super().__init__(app)
        self.font = pygame.font.Font(None, 50)

        self.ui_context.add_widget(Button("Edit Tree", (100, 100), (200, 50), self.to_tree_editor))
        self.ui_context.add_widget(Button("Edit Timeline", (100, 200), (200, 50), self.to_timeline_editor))
        self.ui_context.add_widget(Button("Character Sheets", (100, 300), (200, 50), self.to_character_sheets))
        self.ui_context.add_widget(Button("Quit", (100, 400), (200, 50), self.app.quit))

    def to_tree_editor(self):
        from states.tree_editor import TreeEditor
        self.app.state_manager.change_state(TreeEditor(self.app))

    def to_timeline_editor(self):
        from states.timeline_editor import TimelineEditor
        self.app.state_manager.change_state(TimelineEditor(self.app))

    def to_character_sheets(self):
        from states.character_sheet import CharacterSheet
        self.app.state_manager.change_state(CharacterSheet(self.app))
