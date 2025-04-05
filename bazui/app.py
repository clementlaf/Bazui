import pygame
from bazui.state_manager import StateManager
from bazui.app_state import AppState
from bazui.library import ImageLibrary

class App:
    def __init__(self, app_state=None):
        if app_state is not None:
            self.app_state = app_state
        else:
            self.app_state = AppState()
        self.screen = pygame.display.set_mode(self.app_state.screen_size, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state_manager = StateManager(self)
        self.library = ImageLibrary()  # Library for storing images

    def run(self):
        while self.running:
            self.update()
            self.state_manager.handle_events()
            self.state_manager.update()
            self.state_manager.draw(self.screen)
            pygame.display.flip()
            fps = self.clock.tick(60)
            pygame.display.set_caption(f"FPS: {1/fps*1000:.2f}")

    def quit(self, widget):
        self.running = False

    def update(self):
        self.app_state.screen_size = self.screen.get_size()
        self.app_state.mouse_pos = pygame.mouse.get_pos()
