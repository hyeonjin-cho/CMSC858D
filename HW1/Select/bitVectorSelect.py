########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Implementing bit vector select
# Last updated: 10/26/2019
########################################################################

# Packages installed
from BitVector import BitVector
from SelectSupport import SelectSupport
import random
import math
import time
import csv
import sys

# set seed for practice
#random.seed(100)


def btSelect():

	SIZE = random.randrange(1000,100000)

	# randomly generate bit-vector with SIZE
	bv = BitVector(intVal=64)
	bv = bv.gen_random_bits(SIZE)
	TARGET_RANK = random.randrange(0,bv.count_bits())

	# class of SelectSupport: make Rs, Rb, Rp tables
	select = SelectSupport(bv, SIZE)

	'''
	# print bitvector
	print(bv)
	'''

	start = time.time()
	SELECT = select.select_rankOf(bv, TARGET_RANK)
	end = time.time()
	timeCost = end - start
	bitSize = sys.getsizeof(SELECT)

	return SIZE, SELECT, bitSize

# repeat btSelect() n times and store in csv file
for i in range(1000):
	if __name__ == '__main__':
		test = btSelect()
	with open("text_select.csv", 'a') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(test)
csvFile.close()
