########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW2: Bloom filter build class
# Last updated: 11/26/2019
########################################################################

# Packages installed
import math
import bitarray
import mmh3

class BFbuild():
	def __init__(self, fpr, numKeys):
		self.p = fpr
		self.n = numKeys
		self.m = math.ceil((-self.n*math.log(self.p))/(math.log(2)**2))
		self.k = math.ceil((self.m/self.n)*math.log(2))

		self.bitarray = bitarray.bitarray(self.m)
		self.bitarray.setall(0)

	def insert(self, item):
		for i in range(self.k):
			index = mmh3.hash(item, i) % (self.m)
			self.bitarray[index] = '1'
		return self.bitarray

