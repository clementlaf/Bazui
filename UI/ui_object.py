"""This module contains the UiObject class,
 which is the base class for all the UI objects in the UI module"""

import pygame as pg
from UI.vector import Vector as vec
from UI.link import get

class Builder:
    def __init__(self):
        self.params = {
            "pos_type": "relative",   # relative, absolute
            "background_color": None, # None, color
            "border_color": None,     # None, color
            "border_width": 0,        # 0, int
            "border_radius": 0        # 0, int, [int, int, int, int]
        }

    def __getitem__(self, key: str):
        return self.params[key]
    def __setitem__(self, key: str, value):
        self.params[key] = value

    @property
    def items(self)-> list:
        """Return the items of the builder

        Returns:
            list: The items of the builder
        """

        return self.params.items()


class UiObject:
    def __init__(self, pos: vec, size: vec, builder: Builder):
        self.pos = pos
        self.size = size
        for key, value in builder.items:
            setattr(self, key, value)

    def draw(self, screen: pg.Surface, position: vec):
        """Draw the object on the screen

        Args:
            screen (pg.Surface): _description_
            position (vec): _description_
        """

        if self.background_color is not None:
            pg.draw.rect(screen, self.background_color, pg.Rect(get(position).to_tuple(), get(self.size).to_tuple()), 0, self.border_radius)
        if self.border_width != 0 and self.border_color is not None:
            pg.draw.rect(screen, self.border_color, pg.Rect(get(position).to_tuple(), get(self.size).to_tuple()), self.border_width, self.border_radius)

    def is_under_point(self, position: vec, point: vec)-> bool:
        """Check if the point is under the object

        Args:
            position (vec): The UI object position, relative to the screen
            point (vec): The point to check

        Returns:
            bool: True if the point is under the object, False otherwise
        """

        rect = pg.Rect(get(position).to_tuple(), get(self.size).to_tuple())
        return rect.collidepoint(get(point).to_tuple())

    def is_under_rect(self, position: vec, rect: pg.Rect)-> bool:
        """Check if the object is under the rect

        Args:
            position (vec): The UI object position, relative to the screen
            rect (pg.Rect): The rect to check

        Returns:
            bool: True if the object is under the rect, False otherwise
        """

        return pg.Rect(get(position).to_tuple(), get(self.size).to_tuple()).colliderect(rect)

    def intersection(self, position: vec, rect: pg.Rect)-> pg.Rect:
        """Return the intersection between the object and the rect

        Args:
            position (vec): The UI object position, relative to the
            rect (pg.Rect): The rect to check

        Returns:
            pg.Rect: The intersection between the object and the rect 
        """

        return pg.Rect(get(position).to_tuple(), get(self.size).to_tuple()).clip(rect)
