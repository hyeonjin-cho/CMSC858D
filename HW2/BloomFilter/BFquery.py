########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW2: Bloom filter query class
# Last updated: 11/26/2019
########################################################################

# Packages installed
import math
import bitarray
import mmh3

class BFquery():
	def __init__(self, m, k, queryData, bitarray):
		self.m = m
		self.k = k
		self.queryData = queryData
		self.bitarray = bitarray

		self.queryOut = self.query(self.queryData, self.bitarray)

	def query(self, item, bitarray):
		setBool = True # initially set to True because false positives are allowed
		for i in range(self.k):
			index = mmh3.hash(item, i) % self.m
			if bitarray[index] == '0':
				setBool = False
				return setBool
		return setBool

