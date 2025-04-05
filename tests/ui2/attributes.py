
class FIXED:
    def __init__(self, value=0):
        self.value = value
    def __call__(self):
        return self.value

class FIT:
    def __init__(self, min=0, max=float("inf")):
        self.min = min
        self.max = max

class GROW:
    def __init__(self, min=0, max=float("inf")):
        self.min = min
        self.max = max

class Padding:
    def __init__(self, top=0, right=0, bottom=0, left=0):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def on_axis(self, axis):
        return (self.left, self.right) if axis == 0 else (self.top, self.bottom)

def minmax(value, min, max):
    return min if value < min else max if value > max else value
