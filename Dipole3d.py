from Vector3 import Vector3


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
