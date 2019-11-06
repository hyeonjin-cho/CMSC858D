########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Creating class Rank for WaveletTree
# Last updated: 11/5/2019
########################################################################

class Rank():
	def __init__(self, wtTable, index, interval):
		self.rank(wtTable, index, 1, 0, interval)
		print(wtTable)
		#print(wtTable[2][1])
		#print(wtTable[1][0][index])

	def rank1(self, bv, index):
		count = 0
		for i in range(0, index+1):
			if bv[i] == '1':
				count += 1
		return count

	def rank0(self, bv, index):
		count = 0
		for i in range(0, index+1):
			if bv[i] == '0':
				count += 1
		return count

	
	def rank(self, wtTable, index, i, j, interval):
		#while i <= max(wtTable.keys()):
		print(interval)
		if wtTable[i][j][index] == '1':
			#print(self.rank1(wtTable[i][j], index))
			#print(wtTable[i][j])
			occ = self.rank1(wtTable[i][j], index)
			i += 1
			j = 1
			print(occ)
			#self.rank(wtTable[i][j], occ-1, i, j)
		else:
			#print(self.rank0(wtTable[i][j], index))
			occ = self.rank0(wtTable[i][j], index)
			i += 1
			j = 0
			print(occ)
			#self.rank(wtTable[i][j], occ-1, i, j)


