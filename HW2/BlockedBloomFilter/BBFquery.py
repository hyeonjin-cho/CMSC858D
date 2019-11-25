########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW2: Blocked Bloom filter query class
# Last updated: 11/25/2019
########################################################################

# Packages installed
import math
import bitarray
import mmh3

class BBFquery():
	def __init__(self, m, k, b, queryData, bitList):
		self.m = m
		self.k = k
		self.b = b
		self.queryData = queryData
		self.bitList = bitList

		#print(self.k)
		#print(self.bitList)
		#print(self.queryData)

		self.queryOut = self.query(self.queryData, self.bitList)

	def query(self, item, bitList):
		setBool = True # initially set to True because false positives are allowed
		block = mmh3.hash(item, 0) % (self.b)
		for i in range(1, self.k):
			index = mmh3.hash(item, i) % 512
			if bitList[block][index] == '0':
				setBool = False
				return setBool
		return setBool

