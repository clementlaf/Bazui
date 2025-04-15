from bazui.ui.link import LinkByMethod as LM, get

def horizontal_adjust(widgets, start_pos):
    for i, widget in enumerate(widgets):
        if i == 0:
            widget.pos = start_pos
        else:
            prev_widget = widgets[i - 1]
            widget_pos_link = LM(prev_widget, lambda x, prev_widget=prev_widget: (get(x.pos)[0] + get(prev_widget.size)[0], get(x.pos)[1]))
            widget.pos = widget_pos_link

def vertical_adjust(widgets, start_pos):
    for i, widget in enumerate(widgets):
        if i == 0:
            widget.pos = start_pos
        else:
            prev_widget = widgets[i - 1]
            widget_pos_link = LM(prev_widget, lambda x, prev_widget=prev_widget: (get(x.pos)[0], get(x.pos)[1] + get(prev_widget.size)[1]))
            widget.pos = widget_pos_link
