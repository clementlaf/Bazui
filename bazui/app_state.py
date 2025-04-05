
class AppState:
    """Global application state. Defaults here."""
    def __init__(self):
        self.screen_size = (800, 600)
        self.background_color = "#1E1E1E"
        self.text_font = None

        # parameters
        self.undo_stack_max_size = 20
        self.redo_stack_max_size = 20
        self.max_move_click_distance = 10

        # states
        self.dragged_widget = None
        self.mouse_pos = (0, 0)
        self.clicked_widget = None
        self.clicked_widget_pos = (0, 0)
