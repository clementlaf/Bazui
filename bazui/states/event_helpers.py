
def consume_event(widget):
    """used to consume event on action on a widget
    """

    return True

def no_selection():
    """used to prevent text selection in text widgets
    """
    return None

def spawn_widget_func(spawned_widget):
    """used to spawn a widget on click
    """
    return lambda widget: widget.set_child(spawned_widget)
def despawn_widget_func(spawned_widget):
    """used to despawn a widget on click
    """
    return lambda widget: widget.remove_child(spawned_widget)
def deselect_and_despawn_widget_func(spawned_widget):
    """used to deselect and despawn a widget on click
    """
    def myfunc(widget):
        widget.remove_child(spawned_widget)
        widget.checked = False
        return True
    return myfunc
