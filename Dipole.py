from Vector2 import Vector2
from math import sin, cos
R = 0.01

class Dipole2D:
	def __init__(self, loc, theta, R, size, moi, clockwise: bool=False):
		"""
		Initialize the Dipole2D object.
		
		:param loc: Initial location of the dipole
		:param theta: Initial orientation angle of the dipole
		:param R: Some parameter R (not used in the current implementation)
		:param size: Size of the dipole
		:param moi: Moment of inertia of the dipole
		:param clockwise: True if theta grows clockwise, False otherwise
		"""
		self.size = size
		self.moi = moi
		self.loc = loc
		self.theta = theta
		self.R = R
		self.omega: float = 0  # Angular velocity of the dipole
		self.orientation = -1 if clockwise else 1
		self.update_moment_in_cartesian()  # Calculate the moment in Cartesian coordinates
		self.update_actual_loc()


	def update_moment_in_cartesian(self):
		"""
		Calculate the moment of the dipole in Cartesian coordinates.
		"""
		self.moment = Vector2(-self.orientation*sin(self.theta), cos(self.theta)) * self.size

	def update_actual_loc(self):
		"""
		Returns the actual location of the moment of the dipole.
		
		:return: Vector representing the center location of the dipole
		"""
		self.actual_loc = self.loc + self.R * Vector2(self.orientation*cos(self.theta), sin(self.theta))

	def get_field(self, loc: Vector2):
		"""
		Returns the field the dipole induces at a specific point.
		
		:param loc: Location at which to calculate the field
		:return: Vector representing the induced field at the given location
		"""
		if loc == self.actual_loc:
			return Vector2()  # field at dipole location defined to be zero

		r_hat: Vector2 = loc - self.actual_loc  # Vector from dipole center to the location
		r = abs(r_hat)  # Distance from dipole center to the location
		r_hat /= r  # Normalize r_hat to get the unit vector

		# Calculate the field using the dipole field formula
		return (r_hat * 3 * (self.moment * r_hat) - self.moment) / r**3

	def update(self, dt, B_field: Vector2, external_moment: float = 0, resistance=0):
		"""
		Updates the orientation and angular velocity of the dipole.
		
		:param dt: Time step for the update
		:param B_field: External magnetic field vector
		:param external_moment: External moment applied to the dipole
		:param resistance: Resistance to the dipole's motion
		"""
		# Calculate the net moment acting on the dipole
		# positive moment anticlockwise rotation, so if theta grows clockwise an extra minus sign is required.
		force_moment: float = self.orientation*(self.moment.cross(B_field) + external_moment) - resistance * self.omega
		
		# Update the orientation angle based on the current angular velocity
		self.theta += self.omega * dt
		
		# Recalculate the location and moment
		self.update_moment_in_cartesian()
		self.update_actual_loc()
		
		# Update the angular velocity based on the net moment and moment of inertia
		self.omega += dt * force_moment / self.moi


