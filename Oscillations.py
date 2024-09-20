from Dipole import Dipole, Dipole2D
from Vector3 import Vector3
from Vector2 import Vector2
import time
from math import sin, cos, sqrt, pi
import matplotlib.pyplot as plt
import numpy as np

# mu_0 = 4*pi**10**-7
# m = 0.1
# m *= sqrt(mu_0/(4*pi))
# I = 3/2*0.005*0.021*0.021
m = 0.1 * 10 ** -3
I = 3/2 * 0.005 * 0.021 * 0.021
D = 0.045
M = 0.05
g = 9.8
R = 0.021
DT = 0.0002
SIMULATION_TIME = 10


class DipoleDistribution:

    def __init__(self):
        self.dipoles = []
        self.fixed = []

    def add_dipole(self, dipole, fixed=False):
        self.dipoles.append(dipole)
        self.fixed.append(fixed)

    def update(self):
        for dipole, fixed in zip(self.dipoles, self.fixed):
            if fixed:
                continue
            total_B = dipole.get_field(dipole.loc)
            for other_dipole in self.dipoles:
                total_B += other_dipole.get_field(dipole.loc)
            gravity_moment = 0 #M*g*R*cos(dipole.theta)
            dipole.update(DT, total_B)


def update_and_give_angles(dipoles, *args):
    dipoles.update()
    return [dipole.theta for dipole in args]


def main():
    left_dipole = Dipole2D(Vector2(-D), 0.05, m, I)
    middle_dipole = Dipole2D(Vector2(), 0, m, I)
    right_dipole = Dipole2D(Vector2(D), -0.02, m, I)
    dipoles = DipoleDistribution()
    dipoles.add_dipole(left_dipole)
    dipoles.add_dipole(middle_dipole, fixed=True)
    dipoles.add_dipole(right_dipole)
    num = round(SIMULATION_TIME / DT)
    t = np.linspace(0, SIMULATION_TIME, num)
    left = [0] * num
    right = [0] * num
    index = 0
    while index < num:
        dipoles.update()
        left[index] = left_dipole.theta
        right[index] = right_dipole.theta
        index += 1
    left = np.array(left)
    right = np.array(right)
    plt.plot(t, left, "r")
    plt.plot(t, right, "b")
    plt.show()


if __name__ == '__main__':
    main()
