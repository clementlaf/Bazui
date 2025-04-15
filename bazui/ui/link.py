
class Link:
    def get(self):
        pass

class LinkAttribute(Link):
    def __init__(self, ref, attr, app):
        self._last_frame = -1
        self._cached_value = None
        self.ref = ref
        self.attr = attr
        self.app = app

    def get(self):
        if self._last_frame == self.app.frame_id:
            return self._cached_value
        self._cached_value = get(getattr(self.ref, self.attr))
        self._last_frame = self.app.frame_id
        return self._cached_value

class LinkByMethod(Link):
    def __init__(self, ref, method, app):
        self._last_frame = -1
        self._cached_value = None
        self.ref = ref
        self.method = method
        self.app = app

    def get(self):
        if self._last_frame == self.app.frame_id:
            return self._cached_value
        self._cached_value = get(self.method(self.ref))
        self._last_frame = self.app.frame_id
        return self._cached_value



def get(obj):
    if isinstance(obj, Link):
        return obj.get()
    return obj
