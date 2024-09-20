from Dipole import Dipole2D
from Vector2 import Vector2
from math import sin, cos, sqrt, pi
import matplotlib.pyplot as plt
import numpy as np

M = 0.005
g = 9.8
R = 0.021
m = 0.15 * 10 ** -3  # 10 ** -3 = sqrt(mu_0/4pi)
I = 3/2 * M * R * R
D = 0.064
DT = 0.00003
SIMULATION_TIME = 60

stable_point = -1.4849131468203767


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
            gravity_moment = -M*g*R*cos(dipole.theta)
            resistance = 0.0000
            dipole.update(DT, total_B, gravity_moment, resistance)


def update_and_give_angles(dipoles, *args):
    dipoles.update()
    return [dipole.theta for dipole in args]


def main():
    left_dipole = Dipole2D(Vector2(-D), stable_point + 0.005, m, I)
    middle_dipole = Dipole2D(Vector2(), 0, m, I)
    right_dipole = Dipole2D(Vector2(D), stable_point - 0.002, m, I)
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
    print(left_dipole.theta, right_dipole.theta)
    left = np.array(left)
    right = np.array(right)
    plt.plot(t, left, "r")
    plt.plot(t, right, "b")
    plt.show()


if __name__ == '__main__':
    main()
