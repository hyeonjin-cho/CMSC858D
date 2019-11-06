WaveletTree not yet complete as of 11/6/2019

# wt.py

This python code will accept arguments build, access, rank, and select (only build is complete at this point). Argument build will construct the wavelet tree and store it into an output text file. 

# Usage of wt.py

## build 

with python version 3.7.4, this code can be used as follow in the command-line prompt:

$ python wt.py build *test.txt output.txt*

- *test.txt* contains the input string with which the user wants to construct the wavelet tree. This must be made before wt.py implementation. I started with the example of '0167154263' as in this [paper](https://epubs.siam.org/doi/pdf/10.1137/1.9781611975055.2)
- The first line in the *output.txt* will contain the number of unique characters in the input string. The second line in the *output.txt* will contain the length of the input string, and the third line will contain the blocks of bit-vectors in dictionary format (bit-vector as the value of the dictionary). Each key in the dictionary represents the height of the tree, 1 being the root. The fourth line of the *output.txt* will contain the interval of each bit-vector blocks of the corresponding key. 

## access
not yet complete

## rank
not yet complete

## select
not yet complete
