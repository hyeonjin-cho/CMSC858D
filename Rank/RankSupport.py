########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Implementing bit vector rank
# Last updated: 10/25/2019
########################################################################

# Packages installed
from BitVector import BitVector
from itertools import product
import math


class RankSupport():
	def __init__(self, bv, size):
		# size of bit-vector
		self.SIZE = size
		# sizes of superblock and block
		self.SIZE_S = int(math.ceil((math.log2(self.SIZE)**2)/2))
		self.SIZE_B = int(math.ceil(math.log2(self.SIZE)/2))
	
		# adjust the size of superblocks according to the size of blocks
		if self.SIZE_S % self.SIZE_B != 0:
			self.SIZE_S = int(math.ceil(self.SIZE_S/self.SIZE_B)*self.SIZE_B)

		# number of superblocks and blocks
		self.NUM_S = int(math.ceil(self.SIZE/self.SIZE_S))
		self.NUM_B = int(math.ceil(self.SIZE/self.SIZE_B))

		self.R_s = self.rank_s(bv)
		self.R_b = self.rank_b(bv)
		self.R_p = self.rank_p(bv)

	def countBits(self, bv, start, end):
		bv = bv[start:end]
		count = bv.count_bits()
		return count

	def rank_s(self, bv):
		R_s = []
		start = 0
		for j in range(0, self.SIZE, self.SIZE_S):
			ranks = self.countBits(bv, start, j) # j or end of bv 
			R_s.append(ranks) 
		return R_s

	def rank_b(self, bv):
		R_b = {}
		rankb = [[0 for i in range(int(self.SIZE_S/self.SIZE_B))] for j in range(self.NUM_S)]
		for j in range(0, self.NUM_S):
			for k in range(0, int(self.SIZE_S/self.SIZE_B)):
				if (j*self.SIZE_S+(k*self.SIZE_B)) > self.SIZE:
					count = self.countBits(bv, j*self.SIZE_S, self.SIZE-1)
					break
				else:
					count = self.countBits(bv, j*self.SIZE_S, j*self.SIZE_S+(k*self.SIZE_B))
				rankb[j][k] = count
				
		for i in range(self.NUM_S):
			R_b[i] = rankb[i]
		return R_b


	def rank_p(self, bv):
		bitType = {}
		rankp = [[0 for i in range(self.SIZE_B)] for j in range(2**self.SIZE_B)]
		keys = list(product([0,1], repeat = self.SIZE_B))

		for i in range(0, 2**self.SIZE_B):
			for j in range(0, self.SIZE_B):
				str1 = ''.join(str(x) for x in keys[i])
				bv1 = BitVector(bitstring = str1)
				count = self.countBits(bv1, 0, j+1)
				rankp[i][j] = count
			keys[i] = str1

		
		for i in range(len(keys)):
			bitType[keys[i]] = rankp[i]

		return bitType

	def rank_indexAt(self, bv, index):
		s = self.R_s
		b = self.R_b
		p = self.R_p

		if index >= self.SIZE:
			print("Index out of range!")
			exit()
		else:
			s_index = int(math.floor(index/self.SIZE_S))
			b_index = int(math.floor((index-(self.SIZE_S*s_index))/self.SIZE_B))
			pattern_end = (b_index+1)*self.SIZE_B
			pattern_start = pattern_end - self.SIZE_B
			bitstring = str('0' * 8)
			pattern = BitVector(bitstring=bitstring)
			
			if (s_index*self.SIZE_S)+pattern_end > self.SIZE:
				pattern = bv[(s_index*self.SIZE_S)+pattern_start:self.SIZE]
				bitstring = str('0' * int(self.SIZE_B-len(pattern)))
				pattern = pattern + BitVector(bitstring=bitstring)
			else:
				pattern = bv[(s_index*self.SIZE_S)+pattern_start:(s_index*self.SIZE_S)+pattern_end]
			
			p_index = int(index % self.SIZE_B)

		ranks = s[s_index]
		rankb = b[s_index][b_index]
		rankp = p[str(pattern)][p_index]

		if str(pattern)[p_index] == '1':
			return ranks + rankb + rankp
		else: 
			return 'NA'


	def rank_indexAtforSelect(self, bv, index):
		s = self.R_s
		b = self.R_b
		p = self.R_p

		if index >= self.SIZE:
			print("Index out of range!")
			exit()
		else:
			s_index = int(math.floor(index/self.SIZE_S))
			b_index = int(math.floor((index-(self.SIZE_S*s_index))/self.SIZE_B))
			pattern_end = (b_index+1)*self.SIZE_B
			pattern_start = pattern_end - self.SIZE_B
			bitstring = str('0' * 8)
			pattern = BitVector(bitstring=bitstring)
			
			if (s_index*self.SIZE_S)+pattern_end > self.SIZE:
				pattern = bv[(s_index*self.SIZE_S)+pattern_start:self.SIZE]
				bitstring = str('0' * int(self.SIZE_B-len(pattern)))
				pattern = pattern + BitVector(bitstring=bitstring)
			else:
				pattern = bv[(s_index*self.SIZE_S)+pattern_start:(s_index*self.SIZE_S)+pattern_end]
			
			p_index = int(index % self.SIZE_B)

		ranks = s[s_index]
		rankb = b[s_index][b_index]
		rankp = p[str(pattern)][p_index]

		return ranks + rankb + rankp


