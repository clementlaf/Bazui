import pygame
from state_manager import StateManager
from app_state import AppState
from ui.ui_context import UIContext

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.app_state = AppState()  # Global state
        self.ui_context = UIContext(self.app_state)  # UI manager
        self.state_manager = StateManager(self)

    def run(self):
        while self.running:
            self.state_manager.handle_events()
            self.state_manager.update()
            self.state_manager.draw(self.screen)
            pygame.display.flip()
            fps = self.clock.tick(60)
            pygame.display.set_caption(f"FPS: {1/fps*1000:.2f}")

    def quit(self):
        self.running = False
