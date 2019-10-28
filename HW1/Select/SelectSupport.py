########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Implementing bit vector select
# Last updated: 10/26/2019
########################################################################

# Packages installed
from BitVector import BitVector
from RankSupport import RankSupport
from itertools import product
import math


class SelectSupport():
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

		self.rank = self.callRankSupport(bv, size)
		#return rank

	def callRankSupport(self, bv, size):
		self.R_s = RankSupport.rank_s(self, bv)
		self.R_b = RankSupport.rank_b(self, bv)
		self.R_p = RankSupport.rank_p(self, bv)

		return self.R_s, self.R_b, self.R_p

	def countBits(self, bv, start, end):
		bv = bv[start:end]
		count = bv.count_bits()
		return count

	def getRank(self, bv, rank, size, index_count):
		n = bv[0:size]
		
		if size == 2:
			if RankSupport.rank_indexAt(self, bv, int(math.ceil(size/2)+index_count)) == rank:
				return int(math.ceil(size/2)+index_count)
			else:
				return index_count
		elif RankSupport.rank_indexAtforSelect(self, bv, int(math.ceil(size/2)+index_count)) > rank:
			n = n[0:int(math.ceil(size/2))]
			index_count = index_count
			size = int(math.ceil(size/2))
			return self.getRank(bv, rank, size, index_count)
		elif RankSupport.rank_indexAtforSelect(self, bv, int(math.ceil(size/2)+index_count)) < rank:
			n = n[int(math.ceil(size/2)):size]
			index_count = int(math.ceil(size/2)+index_count)
			size = int(math.ceil(size/2))
			return self.getRank(bv, rank, size, index_count)
		elif RankSupport.rank_indexAtforSelect(self, bv, int(math.ceil(size/2)+index_count)) == rank:
			if RankSupport.rank_indexAt(self, bv, int(math.ceil(size/2)+index_count)) == rank:
				return int(math.ceil(size/2)+index_count)
			else:
				n = n[0:int(math.ceil(size/2))]
				index_count = index_count
				size = int(math.ceil(size/2))
				return self.getRank(bv, rank, size, index_count)

	def select_rankOf(self, bv, rank):
		s = self.R_s
		b = self.R_b
		p = self.R_p

		a = self.rank

		if rank > bv.count_bits():
			return 'NA'
		else:
			return self.getRank(bv, rank, self.SIZE, 0)

