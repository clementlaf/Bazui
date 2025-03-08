"""Grid class for creating a grid of cells in the UI."""

from UI.ui_object import UiObject, Builder
from UI.link import get
from UI.vector import Vector as vec

class Grid(UiObject):
    def __init__(self, pos: vec, size: vec, builder: Builder, rows: int, cols: int, grid_type: str, row_sizes = None, col_sizes = None):
        super().__init__(pos, size, builder)
        self.rows = rows
        self.cols = cols
        self.row_sizes = row_sizes  # list of proportions
        self.col_sizes = col_sizes  # list of proportions
        self.grid_type = grid_type  # "fixed", "auto"
        self.cell_poses = {}
        self.init_build_cells()

    def init_build_cells(self):
        if self.row_sizes is None:
            self.row_sizes = [1/self.rows for _ in range(self.rows)]
        if self.col_sizes is None:
            self.col_sizes = [1/self.cols for _ in range(self.cols)]
        for i, row in enumerate(range(self.rows)):
            for j, col in enumerate(range(self.cols)):
                self.cell_poses[(col, row)] = vec(sum(self.col_sizes[:j])*get(self.size).x,
                                                   sum(self.row_sizes[:i])*get(self.size).y)

    def update(self):
        self.build_cells()

    def build_cells(self):
        if self.grid_type == "fixed":
            for i, row in enumerate(range(self.rows)):
                for j, col in enumerate(range(self.cols)):
                    self.cell_poses[(col, row)] = vec(sum(self.col_sizes[:j])*get(self.size).x,
                                                       sum(self.row_sizes[:i])*get(self.size).y)
        elif self.grid_type == "auto":
            pass
            # TODO: Implement auto grid
