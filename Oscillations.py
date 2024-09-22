from Dipole import Dipole2D
from Vector2 import Vector2
import time
from math import sin, cos, sqrt, pi, exp
import matplotlib.pyplot as plt
import numpy as np
import csv

# Constants
M = 0.005  # Mass of the dipole
g = 9.8  # Acceleration due to gravity
R = 0.0096  # Radius of the dipole
m = 0.15 * 10 ** -3.5  # Magnetic moment
I = 3/2 * M * R * R  # Moment of inertia
D = 0.02  # Distance between dipoles
DT = 0.0001  # Time step for the simulation
SIMULATION_TIME = 20  # Total simulation time

# Stable point for the dipole
stable_point = 1.1203283726727613

# Unit vector in the y direction
y_hat = Vector2(0,1)

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
		"""
		Update the state of each dipole in the distribution.
		"""
		for dipole, fixed in zip(self.dipoles, self.fixed):
			if fixed:
				continue
			total_B = dipole.get_field(dipole.loc)  # Get the magnetic field at the dipole's location
			for other_dipole in self.dipoles:
				total_B += other_dipole.get_field(dipole.loc)  # Sum the fields from all other dipoles
			gravity_moment = -M*g*dipole.center_vector.x*cos(dipole.theta)  # Calculate the gravitational moment
			resistance = 0.0000  # Resistance (damping) term
			dipole.update(DT, total_B, gravity_moment, resistance)  # Update the dipole's state

def update_and_give_angles(dipoles, *args):
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
	left_dipole = Dipole2D(Vector2(-D,0),  -stable_point, R, m, I, Vector2(R,0))
	middle_dipole = Dipole2D(Vector2(0,0.0), 0,0, m, I,Vector2(0,0))
	right_dipole = Dipole2D(Vector2(D,0),  stable_point+0.005, R, m, I, Vector2(-R,0))
	
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
	index = 0
	
	# Run the simulation
	while index < num:
		# Print progress every 1000 steps
		if index % 1000 == 0:
			print(SIMULATION_TIME * index / num)

		dipoles.update()  # Update the dipoles
		left[index] = left_dipole.theta  # Store the angle of the left dipole
		right[index] = right_dipole.theta  # Store the angle of the right dipole

		# Apply damping effect
		alpha = 390
		left_dipole.theta = -stable_point + (left_dipole.theta + stable_point) * exp(-alpha * DT * DT)
		right_dipole.theta = stable_point + (right_dipole.theta - stable_point) * exp(-alpha * DT * DT)
		left_dipole.omega = left_dipole.omega * exp(-alpha * DT * DT)
		right_dipole.omega = right_dipole.omega * exp(-alpha * DT * DT)

		index += 1
	
	# Print final angles of the dipoles
	print(left_dipole.theta, right_dipole.theta)
	
	# Convert lists to numpy arrays for plotting
	left = np.array(left)
	right = np.array(right)
	
	# Plot the angles of the dipoles over time
	plt.plot(t, -left, "r")
	plt.plot(t, right, "b")
	plt.show()
	
	# Save every 100th data point to a CSV file
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
