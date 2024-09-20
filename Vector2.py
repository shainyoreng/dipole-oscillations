class Vector2:

    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        """regular vector addition"""
        return Vector2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        """regular vector subtraction"""
        return Vector2(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        """vector Product"""
        if isinstance(other, Vector2):
            return self.x*other.x + self.y*other.y
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vector2(self.x / other, self.y / other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __abs__(self):
        return (self*self) ** 0.5

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def cross(self, other) -> float:
        return self.x*other.y - self.y*other.x