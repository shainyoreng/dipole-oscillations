from Vector2 import Vector2

class Magnet2:
	# dipoleGenerator is a tuple containing two functions:
	# the first one returns the position of the dipole and the second one returns the moment of the dipole
	def __init__(self, dipole_number, dipoleGenerator, gravitationalTorque , moment_of_inertia, theta0=0, omega0=0,STATIC=False):
		self.dipole_number = dipole_number
		self.getDipolePosition, self.getDipoleMoment = dipoleGenerator
		
		self.getGravTorque = gravitationalTorque

		self.moi = moment_of_inertia  # Moment of inertia
		
		self.theta = theta0  # Initial angle
		self.omega = omega0  # Initial angular velocity

		self.STATIC = STATIC


	def dipoleMagField(self, idx, theta,location):
		# Calculate the field using the dipole field formula
		# The field is calculated at a given position r
		dipole_position = self.getDipolePosition(idx,theta)
		dipole_moment = self.getDipoleMoment(idx,theta)

		if location == self.getDipolePosition(idx,theta):
			return Vector2()  # field at dipole location defined to be zero

		r_hat = location - dipole_position  # Vector from dipole center to the location
		r = abs(r_hat)  # Distance from dipole center to the location
		r_hat /= r  # Normalize r_hat to get the unit vector

		return (r_hat * 3 * (dipole_moment * r_hat) - dipole_moment) / r**3

	# Calculate the magnetic field at a given position r
	def getFieldAt(self, r):
		field = Vector2(0, 0)
		for idx in range(self.dipole_number):
			field += self.dipoleMagField(idx,self.theta,r)
		return field

	# Calculate the torque exerted by other magnets
	def calculateTorque(self, all_magnets,this_id):
		torque = 0
		for idx in range(self.dipole_number):
			for other_id, other_magnet in all_magnets:
				if this_id==other_id:
					continue
				magnetic_field = other_magnet.getFieldAt(self.getDipolePosition(idx,self.theta))
				torque += self.getDipoleMoment(idx,self.theta).cross(magnetic_field)
		return torque

	# Update the angle and angular velocity based on the torque and time step Dt
	def update(self, Dt, all_magnets,magnet_id):
		self.theta += self.omega * Dt
		if self.STATIC:
			return
		self.omega += (self.calculateTorque(all_magnets,magnet_id)+self.getGravTorque(self.theta)) * Dt / self.moi
