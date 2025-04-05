import pygame

class AppState:
    """Global application state."""
    def __init__(self):
        self.screen_size = (800, 600)
        self.background_color = "#1E1E1E"
        self.text_font = "data/fonts/Inconsolata-VariableFont_wdth,wght.ttf"
        self.test_image = pygame.image.load("d:/medias/photos/portable2/1739303837285.jpg")

        # parameters
        self.undo_stack_max_size = 20
        self.redo_stack_max_size = 20

        # states
        self.dragged_widget = None
        self.mouse_pos = (0, 0)

        # size-defined fonts
        self.title1f = pygame.font.Font(self.text_font, 50)
        self.text1f = pygame.font.Font(self.text_font, 20)
