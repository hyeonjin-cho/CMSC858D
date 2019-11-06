########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Creating class WaveletTree
# Last updated: 11/6/2019
########################################################################

# Packages installed
import math 
#from BitVector import BitVector
from Node import Node

class WaveletTree():
	def __init__(self, inputString):
		self.stringList = inputString
		self.SIZE = len(self.stringList) # Number of characters in input string
		self.UNIQ = len(list(sorted(set(self.stringList)))) # Number of unique characters in input string
		self.character = list(sorted(set(self.stringList))) # List of unique characters in input string
		self.numOfHeight = int(math.ceil(math.log2(len(self.character))))

		self.rootNode = Node(None, [], [], []) # no parent at first
		self.rootNode.createWT(self.stringList, self.character, 0)
		self.wtTable = self.rootNode.create_table(self.rootNode.key, self.rootNode.value, self.rootNode.interval)[0]
		self.interval = self.rootNode.create_table(self.rootNode.key, self.rootNode.value, self.rootNode.interval)[1]

		self.wt = {}
		self.int = {}
		for i in range(1,self.numOfHeight+1):
			self.wt[i] = self.wtTable[i]
			self.int[i] = self.interval[i]
