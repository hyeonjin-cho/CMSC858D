########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Creating class Node for WaveletTree
# Last updated: 11/6/2019
########################################################################

# Packages installed
import math
import sys

class Node(object):
	def __init__(self, parent, key, value, interval):
		self.bit_vector = ""
		self.left = None
		self.right = None
		self.parent = parent
		self.key = key
		self.value = value
		self.interval = interval

	def createWT(self, string, alphabet, i):
		left_string = ""
		right_string = ""

		middle = math.floor((len(alphabet)+1)/2)
		left_alphabet = alphabet[0:middle]
		right_alphabet = alphabet[middle:len(alphabet)]

		# If alphabet length is > 2, then we're in a node, leaf otherwise
		if len(alphabet) >= 2:
			for char in string:
				if char in left_alphabet:
					left_string += char
					self.bit_vector += "0"
				else:
					right_string += char
					self.bit_vector += "1"
			i += 1
			self.interval.append(len(self.bit_vector)) 
			self.key.append(i)
			self.value.append(self.bit_vector)
			# Creating new nodes and recursively calling createWT method
			self.left = Node(self, self.key, self.value, self.interval)
			self.left.createWT(left_string, left_alphabet, i)
			self.right = Node(self, self.key, self.value, self.interval)
			self.right.createWT(right_string, right_alphabet, i)

		else:
			# This is a leaf
			i += 1
			for char in string:
				if char in left_alphabet:
					bit_value = "0"
				else:
					bit_value = "1"
				self.bit_vector += bit_value
			self.interval.append(len(self.bit_vector)) 
			self.key.append(i)
			self.value.append(self.bit_vector)

	def create_table(self, key, value, interval):
		wtTable = Dictlist()
		intervalKey = Dictlist()

		for i in range(len(key)):
			wtTable[key[i]] = value[i]

		for i in range(len(key)):
			intervalKey[key[i]] = interval[i]

		for i in range(1, len(intervalKey)+1):
			sumofInterval = 0
			for j in range(0, len(intervalKey[i])):
				sumofInterval += intervalKey[i][j]
				intervalKey[i][j] = sumofInterval

		return wtTable, intervalKey

class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)



