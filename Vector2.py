from math import sin ,cos


class Vector2:
    """
    A class to represent a 2-dimensional vector.
    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.
    """

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
        """Divides the vector by a scalar."""
        return Vector2(self.x / other, self.y / other)

    def __rmul__(self, other):
        """Multiplies a scalar by a vector."""
        return self.__mul__(other)

    def __abs__(self):
        """Returns the magnitude (length) of the vector."""
        return (self*self) ** 0.5

    def __eq__(self, other):
        """Checks if two vectors are equal."""
        return (self.x == other.x) and (self.y == other.y)

    def cross(self, other) -> float:
        """Computes the cross product of two vectors."""
        return self.x*other.y - self.y*other.x

    def rotate(self, angle):
        """rotates the vector by a certain angle"""
        return Vector2(self.x * cos(angle) - self.y * sin(angle), self.x * sin(angle) + self.y * cos(angle))