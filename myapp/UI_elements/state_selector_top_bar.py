from ui.widget import Widget
from ui.text import SingleLineText
from ui.link import get, LinkByMethod as LM, LinkAttribute as LA

def build(screen_size_link, app, font):
    screen_size_link = LA(app.app_state, "screen_size")
    top_bar_size = LM(screen_size_link, lambda x: (get(x)[0], 50))
    top_bar = Widget((0, 0), top_bar_size, "top_bar", app, background_color="#2D2D2D")

    opened_states = app.state_manager.opened_states
    for i, _ in enumerate(opened_states):
        if i == app.state_manager.crt_state:
            state_button = top_bar.set_child(Widget((i * 50, 0), (50, 50), f"state_button_{i}", app, background_color=app.app_state.background_color, on_click=lambda widget, crt=i: widget.app.state_manager.set_active(crt)))
        else:
            state_button = top_bar.set_child(Widget((i * 50, 0), (50, 50), f"state_button_{i}", app, background_color="#3C3C3D", on_click=lambda widget, crt=i: widget.app.state_manager.set_active(crt)))
        pos_link = LM(state_button, lambda x: (x.pos[0] + 12, x.pos[1]))
        state_button.set_child(SingleLineText(pos_link, (50, 50), f"state_button_{i}_text", app, text=str(i), font=font, size_auto_fit=False, text_color=(0, 0, 0)))
    return top_bar
