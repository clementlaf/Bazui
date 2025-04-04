class StateManager:
    def __init__(self, app):
        self.app = app
        self.crt_state = None
        self.opened_states = []

    def set_active(self, state_idx):
        self.crt_state = state_idx
        self.opened_states[state_idx].ui_context.exit_events = True
        self.opened_states[state_idx].on_activation()
    def close_crt_state(self):
        if self.crt_state is not None:
            self.opened_states[self.crt_state].ui_context.exit_events = True
            self.opened_states.pop(self.crt_state)
            if len(self.opened_states) > 0:
                self.set_active(min(self.crt_state, len(self.opened_states) - 1))
            else:
                self.app.quit()
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
