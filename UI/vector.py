import math

class Vector:
    """2D vector class"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("index out of range")

    def __len__(self):
        return 2

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude != 0:
            self.x /= magnitude
            self.y /= magnitude

    def normalized(self):
        v = Vector(self.x, self.y)
        v.normalize()
        return v

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def distance(self, other):
        return (self - other).magnitude()

    def angle(self, other):
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    def rotate(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y

    def rotated(self, angle):
        v = Vector(self.x, self.y)
        v.rotate(angle)
        return v

    def to_tuple(self):
        return self.x, self.y
