import warnings

import pygame as pg

from UI.vector import Vector as vec

class UiObject:
    "main class for all UI objects"
    def __init__(self, position: vec, anchor: str | vec = "topleft", parent=None, size=vec(0, 0)):
        self._position = position
        self._anchor = anchor
        self._parent = parent
        self._size = size

    def _relative_point_position(self, point: vec):
        if self.parent is None:
            return point
        else:
            if self.anchor == "topleft":
                return point + self.parent.position
            if self.anchor == "topright":
                return vec(self.parent.position.x + self.parent.size.x - point.x,
                            self.parent.position.y + point.y)
            if self.anchor == "bottomleft":
                return vec(self.parent.position.x + point.x,
                            self.parent.position.y + self.parent.size.y - point.y)
            if self.anchor == "bottomright":
                return vec(self.parent.position.x + self.parent.size.x - point.x,
                            self.parent.position.y + self.parent.size.y - point.y)
            if self.anchor == "center":
                return vec(self.parent.position.x + self.parent.size.x / 2 - point.x,
                            self.parent.position.y + self.parent.size.y / 2 - point.y)
            if isinstance(self.anchor, vec):
                return vec(self.parent.position.x + self.anchor.x - point.x,
                            self.parent.position.y + self.anchor.y - point.y)
            # wrong anchor
            warnings.warn(f"Wrong anchor: {self.anchor}")
            return point

    def _rect(self):
        return pg.Rect(self.pos.to_tuple(), self.size.to_tuple())
    def _arect(self):
        return pg.Rect(self.apos.to_tuple(), self.size.to_tuple())

    @property
    def pos(self):
        """returns the position of the object

        Returns:
            vec: the position of the object
        """

        return self._position

    @pos.setter
    def pos(self, value):
        self._position = value

    @property
    def apos(self):
        """returns the absolute position of the object

        Returns:
            vec: the absolute position of the object
        """

        return self._relative_point_position(self._position)

    @property
    def size(self):
        """returns the size of the object

        Returns:
            vec: the size of the object
        """

        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def anchor(self):
        """returns the anchor of the object

        Returns:
            str | vec: the anchor of the object
        """

        return self._anchor

    @anchor.setter
    def anchor(self, value):
        self._anchor = value

    @property
    def parent(self):
        """returns the parent of the object

        Returns:
            UiObject: the parent of the object
        """

        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def rect(self):
        """returns the rect of the object

        Returns:
            pg.Rect: the rect of the object
        """

        return self._rect()

    @property
    def arect(self):
        """returns the absolute rect of the object

        Returns:
            pg.Rect: the absolute rect of the object
        """

        return self._arect()
