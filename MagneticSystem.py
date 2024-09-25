from Magnet2 import Magnet2
from math import exp
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

	def update(self):
		for id, magnet in self.magnets:
			magnet.update(self.Dt,self.magnets,id)
	
	def getData(self,magnets_id):
		data = []
		for id in magnets_id:
			data.append(self.getMagnet(id).theta)
		return data

	def damp(self, stable_point,alpha):
		for id, magnet in self.magnets:
			magnet.omega = magnet.omega * exp(-alpha * self.Dt * self.Dt)
