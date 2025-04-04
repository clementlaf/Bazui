import pygame

from ui.widget import Widget
from ui.text import SingleLineText
from ui.link import get, LinkByMethod as LM, LinkAttribute as LA
from states.event_helpers import no_selection

def build(app, font, close_window_func):
    screen_size_link = LA(app.app_state, "screen_size")
    top_bar_size = LM(screen_size_link, lambda x: (get(x)[0], 50))
    top_bar = Widget((0, 0), top_bar_size, "top_bar", app, background_color="#2D2D2D")

    # add window title at top right corner
    title = app.state_manager.opened_states[app.state_manager.crt_state].title
    title_size = app.app_state.title1f.size(title)
    title_pos = LM(top_bar, lambda x: (get(x.pos)[0] + get(x.size)[0] - title_size[0] - 10, get(x.pos)[1]))
    title_text = top_bar.set_child(SingleLineText(title_pos,
                                                  title_size,
                                                  "title_text",
                                                  app,
                                                  text=title,
                                                  font=app.app_state.title1f,
                                                  size_auto_fit=False,
                                                  text_color="#252526",
                                                  on_drag=no_selection))

    opened_states = app.state_manager.opened_states
    x_pos = 0
    for i, _ in enumerate(opened_states):
        txt_color = (0, 0, 0)
        size = (50, 50)
        background_color = "#3C3C3D"
        if i == app.state_manager.crt_state:
            if i != 0:
                size = (50 + 30, 50)
            background_color = app.app_state.background_color
            txt_color = (255, 255, 255)
        state_button = top_bar.set_child(Widget((x_pos, 0),
                                                size,
                                                f"state_button_{i}",
                                                app,
                                                background_color=background_color,
                                                on_click=lambda widget, crt=i: widget.app.state_manager.set_active(crt)
                                                ))
        x_pos += size[0]

        if i == app.state_manager.crt_state and i != 0:
            #add close window button
            pos_link = LM(state_button, lambda x: (get(x.pos)[0] + 60, get(x.pos)[1] + get(x.size)[1]/2 - 5))
            close_button = state_button.set_child(Widget(pos_link,
                                                         (10, 10),
                                                         f"close_button_{i}",
                                                         app,
                                                         on_click=close_window_func,
                                                         has_surface=True,
                                                         render_method=exit_button_draw,
                                                         ))
        
        # draw the number of the state
        pos_link = LM(state_button, lambda x: (x.pos[0] + 12, x.pos[1]))
        state_button.set_child(SingleLineText(pos_link, (50, 50), f"state_button_{i}_text", app, text=str(i), font=font, size_auto_fit=False, text_color=txt_color))
    return top_bar


def exit_button_draw(self):
    # render a red circle innside it
    color = (100, 0, 0)
    if self.hovered:
        color = (255, 0, 0)
    pygame.draw.circle(self.surface, color, (5, 5), 5)
