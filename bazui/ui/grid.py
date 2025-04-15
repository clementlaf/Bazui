import pygame

from bazui.ui.widget import Widget
from bazui.ui.link import get, LinkByMethod, LinkAttribute

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
            self.surface = pygame.Surface(get(self.size), pygame.SRCALPHA)

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


class DynamicContainer(Widget):
    def __init__(self, name, app, **kwargs):
        super().__init__((0, 0), (0, 0), name, app, **kwargs)

    def dynamic_attributes(self):
        if self.childs:
            # child min x and y
            min_x = min_y = 0
            min_x = min(get(child.pos)[0] for child in self.childs if child)
            min_y = min(get(child.pos)[1] for child in self.childs if child)

            max_x = max_y = 0
            max_x = max(get(child.pos)[0] + get(child.size)[0] for child in self.childs if child)
            max_y = max(get(child.pos)[1] + get(child.size)[1] for child in self.childs if child)

            # set the size of the widget to the size of the children
            self.size = (max_x - min_x, max_y - min_y)
            self.pos = (min_x, min_y)
        else:
            self.size = (0, 0)
            self.pos = (0, 0)

    def update(self):
        self.dynamic_attributes()
        super().update()
