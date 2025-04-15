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
        cell_size = LinkAttribute(self, "cell_size", self.app)

        # define links to cell positions
        for i in range(self.grid_shape[0]):
            for j in range(self.grid_shape[1]):
                def el_pos(self, i, j):
                    return (get(self.pos)[0] + self.margin + i * (get(cell_size)[0] + self.padding),
                             get(self.pos)[1] + self.margin + j * (get(cell_size)[1] + self.padding))
                link_to_pos = LinkByMethod(self, lambda x, f=el_pos, gridx=i, gridy=j: f(x, gridx, gridy), self.app)
                self.grid_poses[(i, j)] = link_to_pos

    def grid_pos_to_list_pos(self, grid_pos):
        return grid_pos[0] + grid_pos[1] * self.grid_shape[0]

    def set_child(self, grid_pos, child=None):
        self.childs[self.grid_pos_to_list_pos(grid_pos)] = child
        if child:
            child.pos = self.grid_poses[grid_pos]
        self.ordered_childs = sorted([child for child in self.childs if child is not None], key=lambda x: x.z, reverse=True)
        return child

    @property
    def cell_size(self):
        return ((get(self.size)[0] - 2 * self.margin - (self.grid_shape[0] - 1) * self.padding) / self.grid_shape[0],
                (get(self.size)[1] - 2 * self.margin - (self.grid_shape[1] - 1) * self.padding) / self.grid_shape[1])


class DynamicContainer(Widget):
    def __init__(self, name, app, **kwargs):

        self.margin = 0  # space around childs

        super().__init__((0, 0), (0, 0), name, app, **kwargs)

    def dynamic_attributes(self):
        if self.childs:
            # child min x and y
            min_x = min(get(child.pos)[0] for child in self.childs if child) - self.margin
            min_y = min(get(child.pos)[1] for child in self.childs if child) - self.margin

            max_x = max(get(child.pos)[0] + get(child.size)[0] for child in self.childs if child) + self.margin
            max_y = max(get(child.pos)[1] + get(child.size)[1] for child in self.childs if child) + self.margin

            # set the size of the widget to the size of the children
            self.size = (max_x - min_x, max_y - min_y)
            self.pos = (min_x, min_y)
        else:
            self.size = (0, 0)
            self.pos = (0, 0)

    def update(self):
        self.dynamic_attributes()
        super().update()

class DynamicGrid(Widget):
    def __init__(self, pos, size, name, app, **kwargs):
        super().__init__(pos, size, name, app)

        self.growable_children_indices = []
        self.grid_direction = "horizontal"  # "horizontal" or "vertical"
        self.padding = 0  # padding between grid cells
        self.margin = 0   # margin between grid and widget border

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"DynamicGrid has no attribute {key}")

        self._grid_setup()

    def _grid_setup(self):
        if self.has_surface:
            self.surface = pygame.Surface(get(self.size), pygame.SRCALPHA)

        self.arrange()

    def set_child(self, widget, growable=False):
        super().set_child(widget)

        if growable:
            self.growable_children_indices.append(len(self.childs) - 1)

        return widget

    def arrange(self):
        if self.grid_direction == "horizontal":
            self.arrange_horizontal()
        elif self.grid_direction == "vertical":
            self.arrange_vertical()

        else:
            raise ValueError(f"Invalid grid direction: {self.grid_direction}.")

    def arrange_horizontal(self):

        to_grow_size = get(self.size)[0]

        for i, child in enumerate(self.childs):
            to_grow_size -= get(self.childs[i].size)[0]
        to_grow_size -= self.margin * 2 + self.padding * (len(self.childs) - 1)

        num_growables = len(self.growable_children_indices)
        if num_growables > 0:
            growable_size = to_grow_size / num_growables
        else:
            growable_size = 0

        #adjust sizes
        for i in self.growable_children_indices:
            self.childs[i].size = (get(self.childs[i].size[0]) + growable_size, get(self.childs[i].size)[1])

        # adjust positions
        crt_x = get(self.pos)[0] + self.margin
        for i, child in enumerate(self.childs):
            child.pos = (crt_x, get(self.pos)[1] + self.margin)
            crt_x += get(child.size)[0] + self.padding


    def arrange_vertical(self):
        pass

    def update(self):
        self.arrange()

        super().update()

    def remove_child(self, widget: "Widget"):
        """Remove a child widget from the widget.

        Args:
            widget (Widget): The widget to remove.
        """

        try:
            child_index = self.childs.index(widget)
            if child_index in self.growable_children_indices:
                self.growable_children_indices.remove(child_index)
            self.childs.remove(widget)
            self.ordered_childs = sorted(self.childs, key=lambda x: x.z)
        except ValueError:
            pass
