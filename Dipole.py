from Vector3 import Vector3
from Vector2 import Vector2
from math import sin, cos


class Dipole:

    def __init__(self, loc: Vector3, moment: Vector3, moi: Vector3):
        self.loc = loc
        self.moment = moment
        self.omega: Vector3 = Vector3()
        self.moi = moi

    def get_field(self, point: Vector3) -> Vector3:
        """returns the field the dipole induces at a specific point"""
        if point == self.loc:
            return Vector3()
        r_hat: Vector3 = point - self.loc
        r_hat /= abs(r_hat)
        first_part = r_hat*3*self.moment.dot(r_hat)
        return (first_part - self.moment)

    def update(self, dt, B_field: Vector3, external_moment: float = 0):
        """updates the orientation ond angular velocity of the dipole"""
        force_moment: Vector3 = self.moment * B_field + external_moment
        self.moment += self.omega * self.moment * dt
        self.omega += force_moment.project(self.moment) * dt


class Dipole2D:

    def __init__(self, loc, theta, size, moi):
        self.size = size
        self.moi = moi
        self.loc = loc
        self.theta = theta
        self.omega: float = 0
        self.find_moment_in_cartesian()

    def find_moment_in_cartesian(self):
        self.moment = Vector2(sin(self.theta), cos(self.theta)) * self.size

    def get_field(self, loc: Vector2):
        """returns the field the dipole induces at a specific point"""
        if loc == self.loc:
            return Vector2()
        r_hat: Vector2 = loc - self.loc
        r = abs(r_hat)
        r_hat /= r
        return (r_hat * 3 * (self.moment * r_hat) - self.moment) / r**3

    def update(self, dt, B_field: Vector2, external_moment: float = 0):
        """updates the orientation ond angular velocity of the dipole"""
        force_moment: float = self.moment.cross(B_field)
        self.theta += self.omega * dt
        self.find_moment_in_cartesian()
        self.omega += dt * force_moment / self.moi






