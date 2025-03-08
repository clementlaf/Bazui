

class Link:
    def get(self):
        raise NotImplementedError("Link.get() is not implemented")

class LinkAttribute(Link):
    def __init__(self, source_object: any, source_attribute: str):
        self.source_object = source_object
        self.source_attribute = source_attribute

    def get(self):
        return getattr(self.source_object, self.source_attribute)

class LinkByMethod(Link):
    def __init__(self, source_object: any, method: callable):
        self.source_object = source_object
        self.method = method

    def get(self):
        return self.method(self.source_object)

def get(data_container: any):
    if isinstance(data_container, Link):
        return data_container.get()
    else:
        return data_container
