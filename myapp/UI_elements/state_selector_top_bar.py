from ui.widget import Widget
from ui.text import SingleLineText
from ui.link import get, LinkByMethod as LM

def build(screen_size_link, state_manager, font):
    top_bar = Widget((0, 0), (get(screen_size_link)[0], 50), "top_bar", background_color=(200, 0, 0))

    opened_states = state_manager.opened_states
    for i, state in enumerate(opened_states):
        if i == state_manager.crt_state:
            state_button = top_bar.set_child(Widget((i * 50, 0), (50, 50), f"state_button_{i}", background_color=(255, 0, 0), on_click=lambda widget, crt=i: state_manager.set_active(crt)))
        else:
            state_button = top_bar.set_child(Widget((i * 50, 0), (50, 50), f"state_button_{i}", background_color=(255, 255, 255), on_click=lambda widget, crt=i: state_manager.set_active(crt)))
        pos_link = LM(state_button, lambda x: (x.pos[0] + 12, x.pos[1]))
        state_button.set_child(SingleLineText(pos_link, (50, 50), f"state_button_{i}_text", text=str(i), font=font, size_auto_fit=False, text_color=(0, 0, 0)))
    return top_bar
