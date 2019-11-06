########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Creating class Rank for WaveletTree
# Last updated: 11/6/2019
########################################################################

class Rank():
	def __init__(self, wtTable, wtInterval, index):
		self.rank(wtTable, wtInterval, index, 1, 0)
		print(wtTable)
		print(wtInterval)
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

	
	def rank(self, wtTable, wtInterval, index, i, j):
		#while i <= max(wtTable.keys()):
		#print(wtTable[i][j])
		#print(index)
		if i == 1:
			if wtTable[i][j][index] == '0':
				occ = self.rank0(wtTable[i][j], index)
				j = 0
				i += 1
			else:
				occ = self.rank1(wtTable[i][j], index)
				j = 1
				i += 1
			index = occ-1
			print(wtTable[i][j], index) #ok
			self.rank(wtTable, wtInterval, index, i, j)

		
		elif i == max(wtTable.keys()):
			if wtTable[i][j][index] == '0':
				occ = self.rank0(wtTable[i][j], index)
			else:
				occ = self.rank1(wtTable[i][j], index)
			print("rank is: ", occ)

		else:
			if wtTable[i][j][index] == '0':
				occ = self.rank0(wtTable[i][j], index)
				#print("j:", j)
				j = 0 + 2**(i-1)
				#print("j:", j)
				i += 1
				print(wtTable[i][j], occ-1)
				#print(occ)
				self.rank(wtTable, wtInterval, occ-1, i, j)
			else:
				occ = self.rank1(wtTable[i][j], index)
				#print("j:", j)
				j = 1 + 2**(i-1)
				#print("j:", j)
				i += 1
				#print(wtTable[i][j])
				#print(occ)
				self.rank(wtTable, wtInterval, occ-1, i, j)


