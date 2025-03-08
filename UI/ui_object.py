import pygame as pg
from vector import Vector as vec

class Builder:
    def __init__(self):
        self.params = {
            "pos_type": "relative",
            "background_color": None,
            "border_color": None,
            "border_width": 0,
            "border_radius": 0
        }

    def __setattr__(self, name, value):
        self.params[name] = value


class UiObject:
    def __init__(self, pos: vec, size: vec, builder: Builder):
        self.pos = pos
        self.size = size
        for key, value in builder.items():
            setattr(self, key, value)

    def draw(self, screen: pg.Surface, position: vec):
        """Draw the object on the screen

        Args:
            screen (pg.Surface): _description_
            position (vec): _description_
        """

        pass

    def is_under_point(self, position: vec, point: vec)-> bool:
        """Check if the point is under the object

        Args:
            position (vec): The UI object position, relative to the screen
            point (vec): The point to check

        Returns:
            bool: True if the point is under the object, False otherwise
        """

        rect = pg.Rect(position.to_tuple(), self.size.to_tuple())
        return rect.collidepoint(point.to_tuple())

    def is_under_rect(self, position: vec, rect: pg.Rect)-> bool:
        """Check if the object is under the rect

        Args:
            position (vec): The UI object position, relative to the screen
            rect (pg.Rect): The rect to check

        Returns:
            bool: True if the object is under the rect, False otherwise
        """

        return pg.Rect(position.to_tuple(), self.size.to_tuple()).colliderect(rect)

    def intersection(self, position: vec, rect: pg.Rect)-> pg.Rect:
        """Return the intersection between the object and the rect

        Args:
            position (vec): The UI object position, relative to the
            rect (pg.Rect): The rect to check

        Returns:
            pg.Rect: The intersection between the object and the rect 
        """

        return pg.Rect(position.to_tuple(), self.size.to_tuple()).clip(rect)
