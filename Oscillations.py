from Dipole import Dipole2D
from Vector2 import Vector2
import time
from math import sin, cos, sqrt, pi, exp
import matplotlib.pyplot as plt
import numpy as np
import csv

M = 0.005
g = 9.8
R = 0.0096
m = 0.15 * 10 ** -3.5  # 10 ** -3 = sqrt(mu_0/4pi)
I = 3/2 * M * R * R
D = 0.02
DT = 0.0001
SIMULATION_TIME = 20

stable_point = 1.1203283726727613

y_hat = Vector2(0,1)

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
            gravity_moment = -M*g*dipole.center_vector.x*cos(dipole.theta)
            resistance = 0.0000
            dipole.update(DT, total_B, gravity_moment, resistance)


def update_and_give_angles(dipoles, *args):
    dipoles.update()
    return [dipole.theta for dipole in args]


def main():
    left_dipole = Dipole2D(Vector2(-D,0),  -stable_point, R, m, I, Vector2(R,0))
    middle_dipole = Dipole2D(Vector2(0,0.0), 0,0, m, I,Vector2(0,0))
    right_dipole = Dipole2D(Vector2(D,0),  stable_point+0.005, R, m, I, Vector2(-R,0))
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

        #to see the progress of the simulation
        if index%1000 == 0:
            print(SIMULATION_TIME * index/num)


        dipoles.update()
        left[index] = left_dipole.theta
        right[index] = right_dipole.theta

        #chage the value of alpha to change the damping effect
        alpha = 390
        left_dipole.theta = -stable_point + (left_dipole.theta+stable_point) * exp(-alpha*DT*DT)
        right_dipole.theta = stable_point + (right_dipole.theta-stable_point) * exp(-alpha*DT*DT)
        left_dipole.omega = left_dipole.omega * exp(-alpha*DT*DT)
        right_dipole.omega = right_dipole.omega * exp(-alpha*DT*DT)


        index += 1
    print(left_dipole.theta, right_dipole.theta)
    left = np.array(left)
    right = np.array(right)
    plt.plot(t, -left, "r")
    plt.plot(t, right, "b")
    plt.show()
    
    # Save every 10th data point
    t_reduced = t[::100]
    left_reduced = left[::100]
    right_reduced = right[::100]

    with open('oscillations_data_reduced.csv', 'w', newline='') as csvfile:
        fieldnames = ['time', 'left_theta', 'right_theta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(t_reduced)):
            writer.writerow({'time': t_reduced[i], 'left_theta': left_reduced[i], 'right_theta': right_reduced[i]})

if __name__ == '__main__':
    main()
