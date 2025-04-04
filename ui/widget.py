import pygame
from ui.link import get

class Widget:
    def __init__(self, pos, size, name, app, **kwargs):
        self.pos = pos
        self.size = size
        self.name = name
        self.app = app

        # states
        self.hovered = False  # Can be checked for event management
        self.selected = False  # Can be checked for event management

        # attributes
        self.on_click = None
        self.on_hover = None
        self.on_drag_reception = None
        self.on_drag = None
        self.childs = []
        self.background_color = None
        self.has_surface = False
        self.can_be_selected = False
        self.can_be_dragged = False
        self.contour_color = None
        self.contour_width = 0
        self.corner_radius = 0
        self.render_method = None

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Widget has no attribute {key}")

        self._widget_setup()

    @property
    def rect(self):
        return pygame.Rect(get(self.pos), get(self.size))

    def handle_event(self, event, is_under_parent=True):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.selected = False

        if hasattr(event, "pos"):
            # Perform event handling on childs (all childs are checked)
            consumed = 0
            for child in self.childs:
                if child:
                    consumed += child.handle_event(event, self.rect.collidepoint(event.pos) and is_under_parent)
            if consumed > 0:
                return True
        else:
            for child in self.childs:
                if child:
                    if child.handle_event(event):
                        return True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.can_be_dragged and is_under_parent: # Dragging (no event consumption)
                    self.app.app_state.dragged_widget = self
                if self.can_be_selected or (self.on_click and is_under_parent):
                    if self.can_be_selected:
                        self.selected = True
                    if self.on_click and is_under_parent:
                        self.on_click(self)
                    return True  # Stop event propagation
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.hovered = True
                return True
            else:
                self.hovered = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_drag_reception and self.app.app_state.dragged_widget:
                    self.on_drag_reception(self.app.app_state.dragged_widget)
            self.app.app_state.dragged_widget = None
        return False

    def draw(self, screen: pygame.Surface, origin: tuple[int, int]=(0, 0)):
        """Draw the widget and its childs on the screen.

        Args:
            screen (pygame.Surface): The screen to draw on.
            origin (tuple[int, int], optional): The origin of the surface. Defaults to (0, 0).
        """

        if self.has_surface: # childs draw position is relative to widget position
            rendered_surface = self.access_surface()
            for child in self.childs:
                if child:
                    child.draw(rendered_surface, origin=get(self.pos))
            blit_pos = (get(self.pos)[0] - origin[0], get(self.pos)[1] - origin[1])
            screen.blit(rendered_surface, blit_pos)
        else: # childs draw position is absolute
            if self.background_color:
                pygame.draw.rect(screen, self.background_color, self.rect.move(-origin[0], -origin[1]), border_radius=self.corner_radius)
            if self.contour_color:
                pygame.draw.rect(screen, self.contour_color, self.rect.move(-origin[0], -origin[1]), self.contour_width, border_radius=self.corner_radius)
            for child in self.childs:
                if child:
                    child.draw(screen, origin)

    def _widget_setup(self):
        """ widget initialisation checks and setup """

        if self.on_click and not callable(self.on_click):
            raise AttributeError("on_click must be callable")
        if self.on_hover and not callable(self.on_hover):
            raise AttributeError("on_hover must be callable")

        if self.has_surface:
            self.surface = pygame.Surface(get(self.size), pygame.SRCALPHA)

    def __getitem__(self, widget_name):
        for widget in self.childs:
            if widget.name == widget_name:
                return widget
        return None

    def set_child(self, widget: "Widget")-> "Widget":
        """Add a child widget to the widget.

        Args:
            widget (Widget): The widget to add.

        Returns:
            Widget: The added widget.
        """

        self.childs.append(widget)
        return widget

    def remove_child(self, widget: "Widget"):
        """Remove a child widget from the widget.

        Args:
            widget (Widget): The widget to remove.
        """

        self.childs.remove(widget)

    def update(self):
        """Update the widget and its childs.
        """

        if self.app.app_state.dragged_widget == self and self.can_be_dragged and self.on_drag:
            self.on_drag()
        if self.hovered and self.on_hover:
            self.on_hover()

        if self.has_surface and self.surface.size != get(self.size):
            new_surface = pygame.Surface(get(self.size), pygame.SRCALPHA)
            new_surface.blit(self.surface, (0, 0))
            self.surface = new_surface

        for child in self.childs:
            if child:
                child.update()

    def access_surface(self)-> pygame.Surface:
        """Return the surface of the widget.
        This is called once per frame right before the widget is drawn.

        Returns:
            pygame.Surface: The surface of the widget.
        """
        if self.background_color:
            if self.corner_radius > 0:
                pygame.draw.rect(self.surface, self.background_color, (0, 0, *get(self.size)), border_radius=self.corner_radius)
            else:
                self.surface.fill(self.background_color)
        if self.contour_color:
            pygame.draw.rect(self.surface, self.contour_color, (0, 0, *get(self.size)), self.contour_width, border_radius=self.corner_radius)

        # check for custom render method
        if self.render_method:
            self.render_method(self.surface)
        
        return self.surface
