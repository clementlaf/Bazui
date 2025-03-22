class StateManager:
    def __init__(self, app):
        self.app = app
        self.crt_state = None

    def change_state(self, new_state):
        self.crt_state = new_state

    def handle_events(self):
        if self.crt_state:
            self.crt_state.handle_events()

    def update(self):
        if self.crt_state:
            self.crt_state.update()

    def draw(self, screen):
        if self.crt_state:
            self.crt_state.draw(screen)
