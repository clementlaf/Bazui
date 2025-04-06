
def consume_event(widget):
    """used to consume event on action on a widget
    """

    return True

def method_wrapper(method):
    """used to wrap a method to be used as a callback for an event
    This is useful for methods that are not bound to a widget, such as functions
    that are defined in the app class.
    """
    return lambda widget: method()

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
