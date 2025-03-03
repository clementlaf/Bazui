import pygame as pg

from UIobject import UIobject
from group import Group
from vector import Vector as vec

class Grid(UIobject):
    def __init__(self, position: vec, anchor: str | vec = "topleft", parent=None, size=vec(0, 0), cell_size=vec(0, 0), cell_color=(255, 255, 255), cell_border_color=(0, 0, 0), cell_border_width=1):
        super().__init__(position, anchor, parent, size)
        self.cell_size = cell_size
        self.cell_color = cell_color
        self.cell_border_color = cell_border_color
        self.cell_border_width = cell_border_width
        self._grid = Group([])
        self._create_grid()

    def _create_grid(self):
        for x in range(self.size.x // self.cell_size.x):
            for y in range(self.size.y // self.cell_size.y):
                self._grid.add(UIobject(vec(x * self.cell_size.x, y * self.cell_size.y),
                                         "topleft", self, self.cell_size))

    def draw(self, screen):
        for cell in self._grid.objects:
            pg.draw.rect(screen, self.cell_color, cell.rect, 0)
            pg.draw.rect(screen, self.cell_border_color, cell.rect, self.cell_border_width)
