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
        self.info_tip = None
        self.background_color = None

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Widget has no attribute {key}")

    @property
    def rect(self):
        return pygame.Rect(get(self.pos), get(self.size))

    def handle_event(self, event):

        if hasattr(event, "pos"):
            for child in self.childs:
                if child and self.rect.collidepoint(event.pos): # If event is inside widget
                    if child.handle_event(event):
                        return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
                    return True  # Stop event propagation
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.hover = True
                if self.on_hover:
                    self.on_hover()
                    return True  # Stop event propagation
            else:
                self.hover = False

        return False

    def draw(self, screen):
        if self.background_color:
            pygame.draw.rect(screen, self.background_color, self.rect)
        for child in self.childs:
            if child:
                child.draw(screen)
