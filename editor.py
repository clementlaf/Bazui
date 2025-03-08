"""Application entry point for the Data Tree Editor."""

import os
import pygame as pg
import datatree as dt
from UI.ui_tree import Tree, Node
from UI.ui_object import UiObject, Builder
from UI.vector import Vector as vec
from UI.link import LinkAttribute, LinkByMethod
from UI.grid import Grid


class Editor():
    def __init__(self):

        pg.init()
        pg.display.set_caption("Data Tree Editor")

        self.e = {}
        self.e["project_opened"] = False
        self.e["current_section"] = "1"
        self.e["project_path"] = None
        self.e["project_name"] = ""

        self.screen_width = 800
        self.screen_height = 600
        self.screen_size = vec(self.screen_width, self.screen_height)

        self.ui_tree = Tree()
        self.setup_ui_tree()


        self.screen = pg.display.set_mode(self.screen_size.to_tuple(), pg.RESIZABLE|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            self._events()
            self._update()
            self._draw()
            self.clock.tick(60)

    def _events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
            if event.type == pg.VIDEORESIZE:
                self.screen_width = event.w
                self.screen_height = event.h
                self.screen_size = vec(self.screen_width, self.screen_height)
                pg.display.set_mode((event.w, event.h), pg.RESIZABLE| pg.DOUBLEBUF)

    def _update(self):
        pass

    def _draw(self):
        self.ui_tree.draw(self.screen)
        pg.display.flip()

    def _open_project(self, project_path):
        if os.path.exists(project_path):
            self.e["project_opened"] = True
            self.e["project_path"] = project_path

            project_config = dt.read_config(project_path)
            self.e["project_name"] = project_config["project_name"]
            self.set_title(f"Data Tree Editor - {self.e['project_name']}")
            self.e["current_section"] = project_config["project_root"]

    def _set_title(self, title):
        pg.display.set_caption(title)

    def setup_ui_tree(self):
        main_window_builder = Builder()
        main_window_builder["background_color"] = (50, 50, 50)
        main_window = UiObject(vec(0, 0), LinkAttribute(self, "screen_size"), main_window_builder)
        main_window_node = Node(main_window)
        self.ui_tree.set_root(main_window_node)

        toolbar_builder = Builder()
        toolbar_builder["background_color"] = (30, 30, 30)
        toolbar_builder["border_width"] = 1
        toolbar_builder["border_color"] = (255, 255, 255)
        toolbar_builder["border_radius"] = [0, 0, 10, 10]
        toolbar = UiObject(vec(0, 0), LinkByMethod(self, lambda x : vec(x.screen_width, 50)), toolbar_builder)
        toolbar_node = Node(toolbar)
        self.ui_tree.add_node(toolbar_node, main_window_node)

        test_grid_builder = Builder()
        test_grid_builder["background_color"] = (100, 100, 100)
        test_grid = Grid(vec(0, 50), vec(200, 200), test_grid_builder, 3, 3, "fixed")
        test_grid_node = Node(test_grid)
        self.ui_tree.add_node(test_grid_node, main_window_node)

        child_builders = [Builder() for _ in range(9)]
        for i, builder in enumerate(child_builders):
            col = i/(len(child_builders))*255
            builder["background_color"] = (col, col, col)
        for i in range(9):
            position = LinkByMethod(test_grid,
                                     lambda x, i=i: x.cell_poses[(i%3, i//3)])
            size = LinkByMethod(test_grid,
                                 lambda x, i=i : vec(x.col_sizes[i%3]*x.size.x, x.row_sizes[i//3]*x.size.y))
            child = UiObject(position, size, child_builders[i])
            child_node = Node(child)
            self.ui_tree.add_node(child_node, test_grid_node)


if __name__ == "__main__":
    editor = Editor()
    editor.run()
