########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Implementing bit vector rank
# Last updated: 10/26/2019
########################################################################

# Packages installed
from BitVector import BitVector
from RankSupport import RankSupport
import random
import math
import time
import csv
import sys

# set seed for practice
#random.seed(100)


def btRank():
	SIZE = random.randrange(1000,100000)
	TARGET_INDEX = random.randrange(0,SIZE)

	# randomly generate bit-vector with SIZE
	bv = BitVector(intVal=64)
	bv = bv.gen_random_bits(SIZE)

	# class of RankSupport: make Rs, Rb, Rp tables
	rank = RankSupport(bv, SIZE)

	'''
	# print size of bitvector, superblocks, and blocks
	print("Size of bit vector is: ", rank.SIZE)
	print("Size of superblock is: ", rank.SIZE_S)
	print("Size of block is: ", rank.SIZE_B)
	print("Number of superblocks: ", rank.NUM_S)
	print("Number of blocks: ", rank.NUM_B)
	
	# print bitvector
	print(bv)
	'''

	start = time.time()
	RANK = rank.rank_indexAt(bv, TARGET_INDEX)
	end = time.time()
	timeCost = end - start
	bitSize = sys.getsizeof(RANK)

	return SIZE, RANK, bitSize

# repeat btRank() n times and store in csv file
for i in range(1000):
	if __name__ == '__main__':
		test = btRank()
	with open("text_rank.csv", 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(test)
csvFile.close()


