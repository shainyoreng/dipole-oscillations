from Dipole import Dipole2D
from Vector2 import Vector2
from math import sin, cos, sqrt, pi, exp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import csv

# Constants
M = 0.005  # Mass of the dipole
g = 9.8  # Acceleration due to gravity
R = 0.0096  # Radius of the dipole
m = 0.15 * 10 ** -3.5  # Magnetic moment
I = 3 / 2 * M * R * R  # Moment of inertia
D = 0.04  # Distance between dipoles
DT = 0.001  # Time step for the simulation
SIMULATION_TIME = 10  # Total simulation time
ANIMATION_SPEED = 1  # compared to real time
FRAME_TO_DATA_RATIO = 10  # Number of data points between frames
# most computer can only handle up to 1 frame per millisecond
MOMENT_SIZE_IN_ANIMATION = 0.7  # size of moment vector compared to R

RESISTANCE = 0.00  # Resistance (damping) term
ALPHA = 0  # coefficient for counteracting energy gain

# Stable point for the dipole
stable_point = 3.1538186777539536

y_hat = Vector2(0,1)


def plot_graph(t, left, right):
    # Convert lists to numpy arrays for plotting
    left = np.array(left)
    right = np.array(right)

    # Add axis titles
    plt.xlabel('Time [Sec]')
    plt.ylabel('Angle [Rad]')


    # Change the background color of the plot
    fig = plt.gcf()
    fig.patch.set_facecolor((13 / 255, 17 / 255, 23 / 255))
    ax = plt.gca()
    ax.set_facecolor((13 / 255, 17 / 255, 23 / 255))

    # Set text color to white
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.title.set_color('white')

    # Plot the angles of the dipoles over time
    plt.plot(t, -left, "c")
    plt.plot(t, right, "m")
    plt.show()


def get_location_details(dipole):
    """helper function for animate. re"""
    moment_vector_size = MOMENT_SIZE_IN_ANIMATION * R * dipole.moment.get_normalized()
    return ([*dipole.loc.get_cords(), *dipole.actual_loc.get_cords()],
            [*dipole.actual_loc.get_cords(), *(moment_vector_size + dipole.actual_loc).get_cords()])


def animate(frames, num_frames):
    # Animate the Simulation

    # Set up the figure and axis
    fig, ax = plt.subplots()
    screen_limit = 1.2 * (D+R)
    ax.set_xlim(-screen_limit, screen_limit)
    ax.set_ylim(-screen_limit, screen_limit)

    # Initialize the vectors (arrows) with placeholders
    quivers = [ax.quiver(0, 0, 0, 0, angles='xy', scale_units='xy', scale=1, color=c)
               for c in ['blue', 'blue', 'green', 'green', 'red', 'red']]

    timer_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=14,
                         verticalalignment='top', color='black')

    # Update function for the animation
    def update(frame):
        for i, quiver in enumerate(quivers):
            start_x, start_y, end_x, end_y = frames[frame, i]
            dx, dy = end_x - start_x, end_y - start_y
            quiver.set_offsets([start_x, start_y])
            quiver.set_UVC(dx, dy)
        timer_text.set_text(f"real time: {frame*FRAME_TO_DATA_RATIO*DT:.2f}")
        return quivers

    # Create the animation
    # Interval is milliseconds per frame. In order for it to be accurate, this should be no smaller than 1.
    # The smaller it is the less accurate
    anim = FuncAnimation(fig, update, frames=num_frames, interval=DT*FRAME_TO_DATA_RATIO/ANIMATION_SPEED*1000)

    # Show the animation
    plt.show()


def save_csv(t, left, right, filename):
    # Save the data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['time', 'left_theta', 'right_theta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(t)):
            writer.writerow({'time': t[i], 'left_theta': left[i], 'right_theta': right[i]})


class DipoleDistribution:
    """
    This class represents a distribution of dipoles.
    It manages a list of dipoles and updates their states.
    """

    def __init__(self):
        self.dipoles = []  # List to store dipoles
        self.fixed = []  # List to store whether a dipole is fixed or not

    def add_dipole(self, dipole, fixed=False):
        """
        Add a dipole to the distribution.
        :param dipole: Dipole to be added
        :param fixed: Boolean indicating if the dipole is fixed
        """
        self.dipoles.append(dipole)
        self.fixed.append(fixed)

    def update(self):
        for dipole, fixed in zip(self.dipoles, self.fixed):
            if fixed:
                continue
            total_B = dipole.get_field(dipole.loc)  # Get the magnetic field at the dipole's location
            for other_dipole in self.dipoles:
                total_B += other_dipole.get_field(dipole.loc)  # Sum the fields from all other dipoles
            moment_arm = dipole.actual_loc - dipole.loc
            gravity_moment = M * g * y_hat.cross(moment_arm)  # Calculate the gravitational moment
            dipole.update(DT, total_B, gravity_moment, RESISTANCE)  # Update the dipole's state

    def update_and_give_angles(self, dipoles, *args):
        """
        Update the dipoles and return their angles.
        :param dipoles: DipoleDistribution object
        :param args: List of dipoles
        :return: List of angles of the dipoles
        """
        dipoles.update()
        return [dipole.theta for dipole in args]


def main():
    """
    Main function to run the simulation.
    """
    # Create dipoles
    left_dipole = Dipole2D(Vector2(-D, 0),  0.6, R, m, I, False)
    middle_dipole = Dipole2D(Vector2(0, 0.0), 0, 0, m, I)
    right_dipole = Dipole2D(Vector2(D, 0), -0.6, R, m, I, True)

    # Create a distribution of dipoles
    dipoles = DipoleDistribution()
    dipoles.add_dipole(left_dipole)
    dipoles.add_dipole(middle_dipole, fixed=True)
    dipoles.add_dipole(right_dipole)

    # Simulation parameters
    num = round(SIMULATION_TIME / DT)
    t = np.linspace(0, SIMULATION_TIME, num)
    left = [0] * num
    right = [0] * num
    frames = np.zeros((num, 6, 4))
    index = 0

    # Run the simulation
    while index < num:
        # Print progress every 1000 steps
        if index % 1000 == 0:
            print(SIMULATION_TIME * index / num)

        dipoles.update()  # Update the dipoles
        left[index] = left_dipole.theta  # Store the angle of the left dipole
        right[index] = right_dipole.theta  # Store the angle of the right dipole
        frames[index] = [*get_location_details(left_dipole),
                         *get_location_details(right_dipole),
                         *get_location_details(middle_dipole)]

        # Apply damping effect to counteract energy gain from the approximation (DT!=0)
        # This should be moved into a function somewhere else
        left_dipole.theta = -stable_point + (left_dipole.theta + stable_point) * exp(-ALPHA * DT * DT)
        right_dipole.theta = stable_point + (right_dipole.theta - stable_point) * exp(-ALPHA * DT * DT)
        left_dipole.omega = left_dipole.omega * exp(-ALPHA * DT * DT)
        right_dipole.omega = right_dipole.omega * exp(-ALPHA * DT * DT)

        index += 1

    # Print final angles of the dipoles
    print(left_dipole.theta, right_dipole.theta)
    animate(frames[::FRAME_TO_DATA_RATIO], num//FRAME_TO_DATA_RATIO)
    plot_graph(t, left, right)

    # Save every 100th data point to a CSV file
    if input("Save data to CSV file? (y/n): ") == 'y':
        t_reduced = t[::100]
        left_reduced = left[::100]
        right_reduced = right[::100]
        save_csv(t_reduced, left_reduced, right_reduced, 'oscillations_data_reduced.csv')


if __name__ == '__main__':
    main()
