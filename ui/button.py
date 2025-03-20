import pygame

class Button:
    """Simple UI Button."""
    def __init__(self, text, pos, size, on_click):
        self.text = text
        self.rect = pygame.Rect(pos, size)
        self.on_click = on_click
        self.font = pygame.font.Font(None, 30)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, self.rect.topleft)
