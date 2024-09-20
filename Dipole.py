from Vector2 import Vector2
from math import sin, cos


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

    def update(self, dt, B_field: Vector2, external_moment: float = 0, resistance=0):
        """updates the orientation ond angular velocity of the dipole"""
        force_moment: float = self.moment.cross(B_field) + external_moment - resistance * self.omega
        self.theta += self.omega * dt
        self.find_moment_in_cartesian()
        self.omega += dt * force_moment / self.moi






