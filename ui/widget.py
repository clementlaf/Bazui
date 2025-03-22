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
        self.has_surface = False
        self.surface = None

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Widget has no attribute {key}")

        self._setup()

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

    def draw(self, screen, origin=(0, 0)):
        if self.has_surface: # childs draw position is relative to widget position
            if self.surface.size != get(self.size):
                self.surface = pygame.Surface(get(self.size))

            # Draw widget surface
            if self.background_color:
                self.surface.fill(self.background_color)
            for child in self.childs:
                if child:
                    child.draw(self.surface, origin=get(self.pos))
            blit_pos = (get(self.pos)[0] - origin[0], get(self.pos)[1] - origin[1])
            screen.blit(self.surface, blit_pos)
        else: # childs draw position is absolute
            if self.background_color:
                pygame.draw.rect(screen, self.background_color, self.rect.move(-origin[0], -origin[1]))
            for child in self.childs:
                if child:
                    child.draw(screen, origin)

    def _setup(self):
        """ widget initialisation checks and setup """

        if self.on_click and not callable(self.on_click):
            raise AttributeError("on_click must be callable")
        if self.on_hover and not callable(self.on_hover):
            raise AttributeError("on_hover must be callable")
        if self.info_tip and not isinstance(self.info_tip, str):
            raise AttributeError("info_tip must be a string")

        if self.has_surface:
            self.surface = pygame.Surface(get(self.size))
            self.surface.fill((255, 255, 255))
            self.has_surface = True
