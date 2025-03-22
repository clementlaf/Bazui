
class Link:
    def get(self):
        pass

class LinkAttribute(Link):
    def __init__(self, ref, attr):
        self.ref = ref
        self.attr = attr

    def get(self):
        return getattr(self.ref, self.attr)

class LinkByMethod(Link):
    def __init__(self, ref, method):
        self.ref = ref
        self.method = method

    def get(self):
        return self.method(self.ref)



def get(obj):
    if isinstance(obj, Link):
        return obj.get()
    return obj
