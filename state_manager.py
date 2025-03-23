class StateManager:
    def __init__(self, app):
        self.app = app
        self.crt_state = None
        self.opened_states = []

    def set_active(self, state_idx):
        self.crt_state = state_idx
    def add_state(self, state):
        self.opened_states.append(state)

    def handle_events(self):
        if self.crt_state is not None:
            self.opened_states[self.crt_state].handle_events()

    def update(self):
        if self.crt_state is not None:
            self.opened_states[self.crt_state].update()

    def draw(self, screen):
        if self.crt_state is not None:
            self.opened_states[self.crt_state].draw(screen)
