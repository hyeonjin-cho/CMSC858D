########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW2: Blocked Bloom filter build class
# Last updated: 11/25/2019
########################################################################

# Packages installed
import math
import bitarray
import mmh3

class BBFbuild():
	def __init__(self, fpr, numKeys):
		self.p = fpr
		self.n = numKeys
		self.m = math.ceil((-self.n*math.log(self.p))/(math.log(2)**2))
		self.k = math.ceil((self.m/self.n)*math.log(2))
		self.b = math.ceil(self.m/512)

		self.bitList = []
		for i in range(self.b):
			self.bitarray = bitarray.bitarray(512)
			self.bitarray.setall(0)
			self.bitList.append(self.bitarray)

	def insert(self, item):
		block = mmh3.hash(item, 0) % (self.b)
		for i in range(1, self.k):
			index = mmh3.hash(item, i) % 512
			self.bitList[block][index] = '1'
		return self.bitList

