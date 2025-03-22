import pygame
from state_manager import StateManager
from app_state import AppState

class App:
    def __init__(self):
        pygame.init()
        self.app_state = AppState()  # Global state
        self.screen = pygame.display.set_mode(self.app_state.screen_size, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state_manager = StateManager(self)

    def run(self):
        while self.running:
            self.update()
            self.state_manager.handle_events()
            self.state_manager.update()
            self.state_manager.draw(self.screen)
            pygame.display.flip()
            fps = self.clock.tick(60)
            pygame.display.set_caption(f"FPS: {1/fps*1000:.2f}")

    def quit(self):
        self.running = False

    def update(self):
        self.app_state.screen_size = self.screen.get_size()
