import pygame

from ui.widget import Widget
from ui.link import get, LinkByMethod, LinkAttribute

class Grid(Widget):
    def __init__(self, pos, size, name, app, grid_shape, **kwargs):
        super().__init__(pos, size, name, app)

        # grid attributes
        self.grid_shape = grid_shape
        self.grid_poses = {}

        # attributes
        self.padding = 0  # padding between grid cells
        self.margin = 0   # margin between grid and widget border
        self.grid_type = "fixed_regular"

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Grid has no attribute {key}")

        # grid setup
        self._grid_setup()

    def arrange(self):
        if self.grid_type == "fixed_regular":
            self.arrange_fixed_regular()

    def _grid_setup(self):
        self.childs = [None for _ in range(self.grid_shape[0] * self.grid_shape[1])]
        self.arrange()

        if self.has_surface:
            self.surface = pygame.Surface(get(self.size))

    def arrange_fixed_regular(self):
        # define cell size link
        # def cell_size(self):
        #     return ((get(self.size)[0] - 2 * self.margin - (self.grid_shape[0] - 1) * self.padding) / self.grid_shape[0],
        #             (get(self.size)[1] - 2 * self.margin - (self.grid_shape[1] - 1) * self.padding) / self.grid_shape[1])
        # cell_size = LinkByMethod(self, cell_size)
        cell_size = LinkAttribute(self, "cell_size")

        # define links to cell positions
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                def el_pos(self, i, j):
                    return (get(self.pos)[0] + self.margin + i * (get(cell_size)[0] + self.padding),
                             get(self.pos)[1] + self.margin + j * (get(cell_size)[1] + self.padding))
                link_to_pos = LinkByMethod(self, lambda x, f=el_pos, gridx=i, gridy=j: f(x, gridx, gridy))
                self.grid_poses[(i, j)] = link_to_pos

    def grid_pos_to_list_pos(self, grid_pos):
        return grid_pos[0] + grid_pos[1] * self.grid_shape[0]

    def set_child(self, grid_pos, child=None):
        self.childs[self.grid_pos_to_list_pos(grid_pos)] = child
        if child:
            child.pos = self.grid_poses[grid_pos]
        return child

    @property
    def cell_size(self):
        return ((get(self.size)[0] - 2 * self.margin - (self.grid_shape[0] - 1) * self.padding) / self.grid_shape[0],
                (get(self.size)[1] - 2 * self.margin - (self.grid_shape[1] - 1) * self.padding) / self.grid_shape[1])
