########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Implementing bit vector select
# Last updated: 10/30/2019
########################################################################

# Packages installed
from BitVector import BitVector
from RankSupport import RankSupport
from itertools import product
import math

class SelectSupport():
	def __init__(self, bv, size):
		self.bv = bv

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

		self.rank = RankSupport(bv, size)

	def countBits(self, bv, start, end):
		bv = bv[start:end]
		count = bv.count_bits()
		return count

	def getRank(self, rank, size, index_count):
		if size == 2:
			if RankSupport.rank_indexAt(self.rank, self.bv, int(math.ceil(size/2)+index_count)) == rank:
				return int(math.ceil(size/2)+index_count)
			else:
				return index_count
		elif RankSupport.rank_indexAtforSelect(self.rank, self.bv, int(math.ceil(size/2)+index_count)) > rank:
			index_count = index_count
			size = int(math.ceil(size/2))
			return self.getRank(rank, size, index_count)
		elif RankSupport.rank_indexAtforSelect(self.rank, self.bv, int(math.ceil(size/2)+index_count)) < rank:
			index_count = int(math.ceil(size/2)+index_count)
			size = int(math.ceil(size/2))
			return self.getRank(rank, size, index_count)
		elif RankSupport.rank_indexAtforSelect(self.rank, self.bv, int(math.ceil(size/2)+index_count)) == rank:
			if RankSupport.rank_indexAt(self.rank, self.bv, int(math.ceil(size/2)+index_count)) == rank:
				return int(math.ceil(size/2)+index_count)
			else:
				index_count = index_count
				size = int(math.ceil(size/2))
				return self.getRank(rank, size, index_count)

	def select_rankOf(self, bv, rank):
		if rank > bv.count_bits():
			return 'NA'
		else:
			return self.getRank(rank, self.SIZE, 0)

