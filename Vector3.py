class Vector3:

    def __init__(self, x: float = 0, y: float = 0, z: float =0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """regular vector addition"""
        return Vector3(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        """regular vector subtraction"""
        return Vector3(self.x-other.x, self.y-other.y, self.z-other.z)

    def __mul__(self, other):
        """vector Product"""
        if isinstance(other, Vector3):
            return Vector3(
                self.y*other.z - self.z*other.y,
                self.z*other.x - self.x*other.z,
                self.x*other.y - self.y*other.x
            )
        if isinstance(other, int) or isinstance(other, float):
            return Vector3(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        return Vector3(self.x / other, self.y / other, self.z / other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def dot(self, other) -> float:
        return self.x*other.x + self.y*other.y + self.z*other.z

    def __abs__(self):
        return self.dot(self) ** 0.5

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and self.z == other.z

    def project(self, other):
        return other * self.dot(other)/other.dot(other)

