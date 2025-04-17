
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
        try:
            self._cached_value = get(getattr(self.ref, self.attr))
        except AttributeError:
            self._cached_value = None
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

class MultiLinkByMethod(Link):
    def __init__(self, refs, method, app):
        self._last_frame = -1
        self._cached_value = None
        self.refs = refs
        self.method = method
        self.app = app

    def get(self):
        if self._last_frame == self.app.frame_id:
            return self._cached_value
        self._cached_value = get(self.method(self.refs))
        self._last_frame = self.app.frame_id
        return self._cached_value

def get(obj):
    res = obj
    # if result is a link, get the value of the link
    if isinstance(obj, Link):
        res = obj.get()
    # if result is an iterable, get each element and return it
    if isinstance(res, (tuple, list)):
        return [get(x) for x in res]
    return res
