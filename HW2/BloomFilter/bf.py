########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW2: Implementing Bloom filter
# Last updated: 11/24/2019
########################################################################

# Packages installed
import getopt, sys
from BFbuild import BFbuild
from BFquery import BFquery

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

		bf = BFbuild(fpr, numKeys)
		for i in range(len(keyData)):
			bf.bitarray = bf.insert(keyData[i])
		sys.stdout = open(outputFile, "w")
		print(bf.p)
		print(bf.n)
		print(bf.m)
		print(bf.k)
		print(str(bf.bitarray))

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
		        	inputString = lines[4].strip('\n')
		        	inputString = inputString[inputString.find("(")+2:inputString.find(")")-1]
		    elif currentArgument in ("-q", "--query"):
		    	queryInput = open(currentValue, "r")
		    	queryData = list(queryInput)
		    	for i in range(len(queryData)):
		        	queryData[i] = queryData[i].strip('\n')
		yes = 0
		no = 0
		for i in range(len(queryData)):
			query = BFquery(m, k, queryData[i], inputString)
			print("query (%s): %r" % (queryData[i], query.queryOut))
			if query.queryOut == True:
				yes += 1
			else:
				no += 1
		print("True: ", yes)
		print("False: ", no)
	else:
		print("There is no option \"%s\"" % action)

main()



