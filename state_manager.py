class StateManager:
    def __init__(self, app):
        self.app = app
        self.state = None

    def change_state(self, new_state):
        self.state = new_state

    def handle_events(self):
        if self.state:
            self.state.handle_events()

    def update(self):
        if self.state:
            self.state.update()

    def draw(self, screen):
        if self.state:
            self.state.draw(screen)
