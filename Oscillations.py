from Magnet2 import Magnet2
from MagneticSystem import MagneticSystem
from Vector2 import Vector2
from math import sin, cos, sqrt, pi, exp

from Utils import save_csv
from Plotter import plot_graph

import numpy as np
import csv

# Constants
M = 0.005  # Mass of the dipole
g = 9.8  # Acceleration due to gravity
R = 0.0396  # Radius of the dipole
m = 0.35 * 10 ** -5  # Magnetic moment
I = 3 / 2 * M * R * R  # Moment of inertia
D = 0.04  # Distance between dipoles

# Simulation parameters
DT = 0.001  # Time step for the simulation
SIMULATION_TIME = 1  # Total simulation time
ANIMATION_SPEED = 1  # compared to real time
FRAME_TO_DATA_RATIO = 1  # Number of data points between frames
# most computer can only handle up to 1 frame per millisecond
MOMENT_SIZE_IN_ANIMATION = 0.7  # size of moment vector compared to R

RESISTANCE = 0.00  # Resistance (damping) term
ALPHA = 0  # coefficient for counteracting energy gain

# Stable point for the dipole
stable_point = 3.1538186777539536

MagnetQuality = 10  # Number of dipoles in each magnet

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
    LeftMagnetGenerator = (lambda idx, theta: Vector2(R*idx*cos(theta)/(MagnetQuality-1)-D, R*idx*sin(theta)/(MagnetQuality-1)),
                        lambda idx, theta: Vector2(-sin(theta)*m/MagnetQuality, cos(theta)*m/MagnetQuality))
    LeftMagnet = Magnet2(MagnetQuality, LeftMagnetGenerator, lambda theta: cos(theta)*M*g*R, I,theta0=0.6)

    
    # Right Magnet
    RightMagnetGenerator = (lambda idx, theta: Vector2(D-R*idx*cos(theta)/(MagnetQuality-1), R*idx*sin(theta)/(MagnetQuality-1)),
                        lambda idx, theta: Vector2(sin(theta)*m/MagnetQuality, cos(theta)*m/MagnetQuality))
    RightMagnet = Magnet2(MagnetQuality, LeftMagnetGenerator, lambda theta: -cos(theta)*M*g*R, I,theta0=-0.5)

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
        # Print progress every 1000 steps
        if index % 1000 == 0:
            print(SIMULATION_TIME * index / num)

        # Update the system
        system.update()

        left[index], right[index] = system.getData([Magnet1_id,Magnet2_id])

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
