from Magnet2 import Magnet2
from math import exp

from RungaKutta import approximation_increment_RNK6f7

# MagneticSystem.py


class MagneticSystem:
	def __init__(self,Time_Diffretial=0.001):
		self.magnets = []
		self.next_id = 0
		self.Dt = Time_Diffretial

	def addMagnet(self, magnet):
		magnet_id = self.next_id
		self.magnets.append((magnet_id, magnet))
		self.next_id += 1
		return magnet_id

	def getMagnet(self, magnet_id):
		for id, magnet in self.magnets:
			if id == magnet_id:
				return magnet
		return None

	def update(self,ddtheta1,ddtheta2,magnet1_id,magnet2_id):
		magnet1 = self.getMagnet(magnet1_id)
		magnet2 = self.getMagnet(magnet2_id)

		theta1,theta2,omega1,omega2 = magnet1.theta,magnet2.theta,magnet1.omega,magnet2.omega
		theta1,theta2,omega1,omega2 = approximation_increment_RNK6f7(ddtheta1,ddtheta2,theta1,theta2,omega1,omega2,self.Dt)

		magnet1.theta = theta1
		magnet1.omega = omega1

		magnet2.theta = theta2
		magnet2.omega = omega2
	
	def getData(self,magnets_id):
		data = []
		for id in magnets_id:
			data.append(self.getMagnet(id).theta)
		return data

	def damp(self, stable_point,alpha):
		for id, magnet in self.magnets:
			magnet.omega = magnet.omega * exp(-alpha * self.Dt * self.Dt)
