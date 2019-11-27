########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW2: Implementing Blocked Bloom filter
# Last updated: 11/26/2019
########################################################################

# Packages installed
import getopt, sys
from BBFbuild import BBFbuild
from BBFquery import BBFquery
import time

def main():
	script = sys.argv[0]
	action = sys.argv[1]
	fullCmdArguments = sys.argv[2:]
	argumentList = fullCmdArguments

	if action == 'build':
		unixOpt = "hk:f:n:o:"
		shortOpt = ["h", "k", "f", "n", "o"]
		gnuOpt = ["help", "key=", "fpr=", "numKeys=", "output="]
		explanationOpt = ["options of the program listed", "(required) input key file", "(required) false positive rate (choose from: 0 < fpr < 1)", "(required) number of keys", "(required) path to output file"]

		try:
		    optList, values = getopt.getopt(argumentList, unixOpt, gnuOpt)
		except getopt.error as err:
		    print(str(err))
		    for i in range(len(gnuOpt)):
		    	print("--%s or -%s: %s" % (gnuOpt[i], shortOpt[i], explanationOpt[i]))
		    sys.exit(2)

		for currentArgument, currentValue in optList:
		    if currentArgument in ("-h", "--help"):
			    for i in range(len(gnuOpt)):
			    	print("--%s or -%s: %s" % (gnuOpt[i], shortOpt[i], explanationOpt[i]))
		    elif currentArgument in ("-k", "--key"):
		        keyFile = open(currentValue, "r")
		        keyData = list(keyFile)
		        for i in range(len(keyData)):
		        	keyData[i] = keyData[i].strip('\n')
		    elif currentArgument in ("-f", "--fpr"):
		    	fpr = float(currentValue)
		    elif currentArgument in ("-n", "--numKeys"):
		    	numKeys = int(currentValue)
		    elif currentArgument in ("-o", "--output"):
		    	outputFile = currentValue

		bf = BBFbuild(fpr, numKeys)
		for i in range(len(keyData)):
			bf.bitList = bf.insert(keyData[i])
		sys.stdout = open(outputFile, "w")
		print(bf.p)
		print(bf.n)
		print(bf.m)
		print(bf.k)
		print(bf.b)
		print(list(bf.bitList))

	elif action == 'query':
		unixOpt = "hi:q:"
		shortOpt = ["h", "i", "q"]
		gnuOpt = ["help", "input=", "query="]
		explanationOpt = ["options of the program listed", "(required) input bitarray text file", "(required) query text file"]

		try:
		    optList, values = getopt.getopt(argumentList, unixOpt, gnuOpt)
		except getopt.error as err:
		    print(str(err))
		    for i in range(len(gnuOpt)):
		    	print("--%s or -%s: %s" % (gnuOpt[i], shortOpt[i], explanationOpt[i]))
		    sys.exit(2)

		for currentArgument, currentValue in optList:
		    if currentArgument in ("-h", "--help"):
			    for i in range(len(gnuOpt)):
			    	print("--%s or -%s: %s" % (gnuOpt[i], shortOpt[i], explanationOpt[i]))
			    sys.exit(2)
		    elif currentArgument in ("-i", "--input"):
		        with open(currentValue, "r") as inputFile:
		        	lines = inputFile.readlines()
		        	m = int(lines[2].strip('\n'))
		        	k = int(lines[3].strip('\n'))
		        	b = int(lines[4].strip('\n'))
		        	inputString = lines[5].strip('\n')
		        	inputList = []
		        	a = inputString.split(',')
		        	for i in range(0, b):
		        		temp = a[i]
		        		temp = temp[temp.find("(")+2:temp.find(")")-1]
		        		inputList.append(temp)
		    elif currentArgument in ("-q", "--query"):
		    	queryInput = open(currentValue, "r")
		    	queryData = list(queryInput)
		    	for i in range(len(queryData)):
		        	queryData[i] = queryData[i].strip('\n')
		yes = 0
		no = 0
		start = time.time()
		for i in range(len(queryData)):
			query = BBFquery(m, k, b, queryData[i], inputList)
			print("query (%s): %r" % (queryData[i], query.queryOut))
			if query.queryOut == True:
				yes += 1
			else:
				no += 1
		end = time.time()
		timeCost = (end - start)/float(len(queryData))
		
		print("True: ", yes)
		print("False: ", no)
		print("Time cost: ", timeCost)
	else:
		print("There is no option \"%s\"" % action)

main()
