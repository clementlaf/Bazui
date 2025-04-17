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
                # If the event was consumed by a widget, break the loop
                break
            self.hotkeys.handle_events(event)

    def update(self):
        self.ui_context.update()

    def draw(self, screen):
        screen.fill(self.app_state.background_color)
        self.ui_context.draw(screen)

    def on_activation(self):
        """Called when the state is activated."""
        pass
