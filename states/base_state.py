import pygame
from ui.ui_context import UIContext

class BaseState:
    def __init__(self, app):
        self.app = app
        self.app_state = app.app_state  # Access shared state
        self.ui_context = UIContext(self.app_state)  # Access UI manager

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.quit()
            self.ui_context.handle_events(event)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill(self.app_state.background_color)
        self.ui_context.draw(screen)
