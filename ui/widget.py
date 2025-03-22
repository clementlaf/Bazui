import pygame
from ui.link import get

class Widget:
    def __init__(self, pos, size, **kwargs):
        self.pos = pos
        self.size = size

        # states
        self.hover = False

        # attributes
        self.on_click = None
        self.on_hover = None
        self.childs = []
        self.minx_size = None
        self.miny_size = None

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Widget has no attribute {key}")

    @property
    def rect(self):
        return pygame.Rect(get(self.pos), get(self.size))

    def handle_event(self, event):

        for child in self.childs:
            if self.rect.collidepoint(event.pos): # If event is inside widget
                if child.handle_event(event):
                    return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                    return True
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.hover = True
                if self.on_hover:
                    self.on_hover()
                    return True
            else:
                self.hover = False

        return False

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
