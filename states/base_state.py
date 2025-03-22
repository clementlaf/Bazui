import pygame

class BaseState:
    def __init__(self, app):
        self.app = app
        self.ui_context = app.ui_context  # Access UI manager
        self.app_state = app.app_state  # Access shared state

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
