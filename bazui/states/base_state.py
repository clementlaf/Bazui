import pygame
from bazui.ui.ui_context import UIContext
from bazui.states.hotkey_manager import HotkeyManager

class BaseState:
    def __init__(self, app):
        self.app = app
        self.app_state = app.app_state  # Access shared state
        self.ui_context = UIContext(self.app_state)  # Access UI manager
        self.hotkeys = HotkeyManager() # Access hotkey manager

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.quit(None)
            res = self.ui_context.handle_events(event)
            if res:
                continue
            self.hotkeys.handle_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # left click not consumed by any widget
                currently_selected_widget = self.app.app_state.selected_widget
                if currently_selected_widget is not None and currently_selected_widget.on_deselect:
                    currently_selected_widget.on_deselect(currently_selected_widget)
                self.app_state.selected_widget = None

    def update(self):
        self.ui_context.update()

    def draw(self, screen):
        screen.fill(self.app_state.background_color)
        self.ui_context.draw(screen)

    def on_activation(self):
        """Called when the state is activated."""
        pass
