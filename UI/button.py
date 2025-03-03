import pygame as pg
import UIobject

class Button(UIobject.UIobject):

    def point_in(self, point):
        """checks if a point is inside the button

        Args:
            point (vec): the point to check

        Returns:
            bool: whether the point is inside the button
        """
        return self.arect.collidepoint(point)
    
    def rect_in(self, rect):
        """checks if a rect is inside the button

        Args:
            rect (pg.Rect): the rect to check

        Returns:
            bool: whether the rect is inside the button
        """
        return self.arect.colliderect(rect)
    
    def intersection(self, rect):
        """returns the intersection of the button and a rect

        Args:
            rect (pg.Rect): the rect to check

        Returns:
            pg.Rect: the intersection of the button and the rect
        """
        return self.arect.clip(rect)
