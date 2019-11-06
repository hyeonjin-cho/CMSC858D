########################################################################
# Author: Hyeon Jin Cho
# CMSC858D_HW1: Implementing WaveletTree
# Last updated: 11/6/2019
########################################################################

# Packages installed
import sys
import yaml
from BitVector import BitVector
from RankSupport import RankSupport
from SelectSupport import SelectSupport
from WaveletTree import WaveletTree
#from Access import Access
from Rank import Rank

def WTquery():
    script = sys.argv[0]
    action = sys.argv[1]
    
    if action == 'build':
        filename = sys.argv[2]
        outputfile = sys.argv[3] 
        data = open(filename, "r")
        inputString = data.read() # type(inputString): str
        inputString = list(inputString)

        for i in range(len(inputString)):
            if inputString[i] == ' ':
                inputString[i] = '_'
        wt = WaveletTree(inputString)
        sys.stdout = open(outputfile, "w")
        print(wt.UNIQ)
        print(wt.SIZE)
        print(wt.character)
        print(wt.wt)
        print(wt.int)

    elif action == 'access':
        wtfile = sys.argv[2]
        index = sys.argv[3]
        with open(wtfile, "r") as df:
            lines = df.readlines()
            s = lines[3].rstrip('\n')
            wtTable = yaml.load(s, Loader=yaml.FullLoader)
        #wtAccess = Access(wtTable, index)
            
    elif action == 'rank':
        wtfile = sys.argv[2]
        index = int(sys.argv[3])
        with open(wtfile, "r") as df:
            lines = df.readlines()
            a = lines[3].rstrip('\n')
            wtTable = yaml.load(a, Loader=yaml.FullLoader)
            b = lines[4].rstrip('\n')
            wtInterval = yaml.load(b, Loader=yaml.FullLoader)
        #print(wtTable)
        wtRank = Rank(wtTable, wtInterval, index)

    elif action == 'select':
        values = data

if __name__ == '__main__':
   test = WTquery()



