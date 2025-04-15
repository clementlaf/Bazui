from bazui.ui.link import LinkAttribute as LA, LinkByMethod as LM, get

def horizontal_adjust(widgets, start_pos):
    app = widgets[0].app
    for i, widget in enumerate(widgets):
        if i == 0:
            widget.pos = start_pos
        else:
            prev_widget = widgets[i - 1]
            widget_pos_link = LM(prev_widget, lambda x, prev_widget=prev_widget: (get(x.pos)[0] + get(prev_widget.size)[0], get(x.pos)[1]), app)
            widget.pos = widget_pos_link

def vertical_adjust(widgets, start_pos):
    app = widgets[0].app
    for i, widget in enumerate(widgets):
        if i == 0:
            widget.pos = start_pos
        else:
            prev_widget = widgets[i - 1]
            widget_pos_link = LM(prev_widget, lambda x, prev_widget=prev_widget: (get(x.pos)[0], get(x.pos)[1] + get(prev_widget.size)[1]), app)
            widget.pos = widget_pos_link
