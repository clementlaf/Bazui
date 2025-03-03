import pygame as pg
import datatree as dt
import os

from UI.UIobject import UIobject, link

class Editor():
    def __init__(self):

        pg.init()
        pg.display.set_caption("Data Tree Editor")

        self.e = {}
        self.e["project_opened"] = False
        self.e["current_section"] = "1"
        self.e["project_path"] = None
        self.e["project_name"] = ""
        self.e["background_color"] = (30, 30, 30)


        self.screen = pg.display.set_mode((800, 600), pg.RESIZABLE|pg.DOUBLEBUF|pg.HWSURFACE)
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

    def _update(self):
        pass

    def _draw(self):
        self.screen.fill(self.e["background_color"])
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

if __name__ == "__main__":
    editor = Editor()
    editor.run()
