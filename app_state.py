class AppState:
    """Global application state."""
    def __init__(self):
        self.screen_size = (800, 600)
        self.background_color = (0, 0, 0)
        self.text_font = "data/fonts/Inconsolata-VariableFont_wdth,wght.ttf"

        # parameters
        self.undo_stack_max_size = 20
        self.redo_stack_max_size = 20

        # states
        self.dragged_widget = None
        self.mouse_pos = (0, 0)
