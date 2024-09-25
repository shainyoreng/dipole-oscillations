from Magnet2 import Magnet2
from MagneticSystem import MagneticSystem
from Vector2 import Vector2
from math import sin, cos, sqrt, pi, exp

from Utils import save_csv
from Plotter import plot_graph, save_as_image

import numpy as np
import csv

# Constants
M = 0.005  # Mass of the dipole
g = 9.8  # Acceleration due to gravity
R = 0.0098  # Radius of the dipole
m = 9 * 10 ** -3.5  # Magnetic moment
I = 3 / 2 * M * R * R  # Moment of inertia
D = 0.04  # Distance between dipoles

# Simulation parameters
DT = 0.0001  # Time step for the simulation
SIMULATION_TIME = 0.1  # Total simulation time
ANIMATION_SPEED = 1  # compared to real time
FRAME_TO_DATA_RATIO = 1  # Number of data points between frames
# most computer can only handle up to 1 frame per millisecond
MOMENT_SIZE_IN_ANIMATION = 0.7  # size of moment vector compared to R

RESISTANCE = 0.00  # Resistance (damping) term
ALPHA = 0  # coefficient for counteracting energy gain

# Stable point for the dipole
stable_point = -3.7

MagnetQuality = 15  # Number of dipoles in each magnet

def main():
    """
    Main function to run the simulation.
    """
    # Create Magnets
    # Center Magnet, (position,moment)
    CenterMagnetGenerator = (lambda idx, theta: Vector2(2*R*idx/(MagnetQuality-1)-R, 0),
                             lambda idx, theta: Vector2(0, m/MagnetQuality))
    CenterMagnet = Magnet2(MagnetQuality, CenterMagnetGenerator, lambda theta: 0, I, STATIC=True)

    # Left Magnet
    LeftMagnetGenerator = (lambda idx, theta: Vector2(2*R*idx*cos(theta)/(MagnetQuality-1)-D,
                                                      2*R*idx*sin(theta)/(MagnetQuality-1)),
                           lambda idx, theta: Vector2(-sin(theta)*m/MagnetQuality,
                                                       cos(theta)*m/MagnetQuality))
    LeftMagnet = Magnet2(MagnetQuality, LeftMagnetGenerator, lambda theta: -cos(theta)*M*g*R, I,theta0=stable_point)
    
    # Right Magnet
    RightMagnetGenerator = (lambda idx, theta: Vector2(D+2*R*idx*cos(theta)/(MagnetQuality-1),
                                                         2*R*idx*sin(theta)/(MagnetQuality-1)),
                            lambda idx, theta:  Vector2(sin(theta)*m/MagnetQuality,
                                                      -cos(theta)*m/MagnetQuality))
    RightMagnet = Magnet2(MagnetQuality, RightMagnetGenerator, lambda theta: -cos(theta)*M*g*R, I,theta0=pi-stable_point)

    # Create the magnetic system
    system = MagneticSystem(DT)
    Magnet1_id = system.addMagnet(LeftMagnet)
    Magnet2_id = system.addMagnet(RightMagnet)
    system.addMagnet(CenterMagnet)

    # Simulation parameters
    num = round(SIMULATION_TIME / DT)
    t = np.linspace(0, SIMULATION_TIME, num)
    left = [0] * num
    right = [0] * num
    index = 0

    # Run the simulation
    while index < num:
        #print(system.getData([Magnet1_id,Magnet2_id]))
        # Print progress every 1000 steps
        if index % 100 == 0:
            print(SIMULATION_TIME * index / num)
            save_as_image(system,'pictures/system'+str(index//100)+'.png',-.05,-0.03,.05,0.03)


        def getAngularAcceleration1(theta1,theta2):
            M1 = system.getMagnet(Magnet1_id)
            M2 = system.getMagnet(Magnet2_id)
            theta10 = M1.theta
            theta20 = M2.theta
            M1.setTheta(theta1)
            M2.setTheta(theta2)
            value = M1.getAngularAcceleration(system.magnets,Magnet1_id)
            M1.setTheta(theta10)
            M2.setTheta(theta20)
            return value

        def getAngularAcceleration2(theta1,theta2):
            M1 = system.getMagnet(Magnet1_id)
            M2 = system.getMagnet(Magnet2_id)
            theta10 = M1.theta
            theta20 = M2.theta
            M1.setTheta(theta1)
            M2.setTheta(theta2)
            value = M2.getAngularAcceleration(system.magnets,Magnet2_id)
            M1.setTheta(theta10)
            M2.setTheta(theta20)
            return value

        # Update the system
        system.update(getAngularAcceleration1,getAngularAcceleration2,Magnet1_id,Magnet2_id)

        left[index], right[index] = system.getData([Magnet1_id,Magnet2_id])
        right[index] = pi-right[index]
        left[index] = left[index]
        # Apply damping effect to counteract energy gain from the approximation (DT!=0)
        # This should be moved into a function somewhere else
        system.damp(stable_point, ALPHA)
        
        index += 1

    # Print final angles of the dipoles
    plot_graph(t, left, right)

    # Save every 100th data point to a CSV file
    if input("Save data to CSV file? (y/n): ") == 'y':
        save_csv(t, left, right, 'oscillations_data_reduced.csv')


if __name__ == '__main__':
    main()
