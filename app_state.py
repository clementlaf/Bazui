class AppState:
    """Global application state."""
    def __init__(self):
        self.window_size = (800, 600)
        self.grid_size = (10, 10)  # Example grid size for UI layout
        self.theme = "dark"
        self.data = {}  # Custom data tree, timeline, character sheets, etc.

    def update_grid_size(self, new_size):
        self.grid_size = new_size
