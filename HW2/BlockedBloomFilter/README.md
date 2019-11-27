blockedbf.py, BBFbuild.py and BBFquery.py import bitarray.py (https://pypi.org/project/bitarray/) and mmh3 (https://pypi.org/project/mmh3/) 

# blockedbf.py

This python code will read an input text file (testKey.txt) to generate Bloom Filter bitarray. There are two command-line arguments for this program. One is ‘build,’ which will build the blocked Bloom Filter, and the other is ‘query,’ which will issue each of the queries in the query file. The specifics of the usage for each command-line arguments are described below. 

# BBFbuild.py

The code contains class BBFbuild(), which imports bitarray and mmh3 package for bit-vector arrays and hash functions, respectively. blockedbf.py ‘build’ argument will pass desired false positive rate and number of unique keys for bitarray size (bloom filter size, m), number of hash function (k), and number of blocks (b) calculations. After setting the size of the bitarray (initially the bitarray is set to all ‘0’), the program will run the hash function k times. Since the value from the hash function will be much bigger than the size of the bloom filter, the program will take the hash function modulo the bloom filter size. The first hash function will be used to determine to which block should the key go. Therefore, the first hash value will take modulo of the number of blocks and the other hash functions will take modulo of the size of the bloom filter. The first result from the first modulo operation (the first hash function) will be the block number, and the rest will be used as the index of the bitarray. 

## Usage of ‘build’

The output of ‘build’ will also be in text file format, containing desired false positive rate, number of unique keys, size of the Bloom Filter bitarray, and the actual bitarray, respectively.
The required options for the command-line argument are:

```
--key= or -k
--fpr= or -f
--numKeys= or -n
--output= or -o
```

The user has to provide with the key input file (--key or -k) in .txt format and desired false positive rate (--fpr= or -f). The numKeys (--numKeys= or -n) is simply the number of unique keys in the key input file. The example of the usage is: 

```
$ python blockedbf.py build -k <test key input> -f <desired false positive rate> -n <num. of unique keys> -o <output>
```

*`-h` or `--help` option will list the options and their descriptions*

## testKey text files

These text file contain input key for bloom filter construction. It is randomly generated using online tool (http://www.unit-conversion.info/texttools/random-string-generator/). I only used first 9 alphabets (all lowercase) to generate 10,000 strings with length 5. There are 6 different numbers of keys in each file: 10K, 20K, 50K, 100K, 200K, 500K, and 1M, all of which are indicated in the name of the files. The number of unique keys in each testKey text file is calculated using python code:

```
>>> len(list(sorted(set(df))))
```
*The testKey text files are identical from the standard Bloom Filter*

## Example

```
$ python blockedbf.py build -k testKey100K.txt -f 0.1 -n 41097 -o output.txt
```
The output.txt will look like this:
```
0.1
41097
196959
4
385 
[bitarray('10010…00100'), bitarray('11101…00101'), bitarray('00000…11110'), bitarray('10010…11101'), …, bitarray('11001…01000')]
```
The numbers in the output.txt are fpr, numKeys, size of bloom filter, number of hash functions, number of blocks and the list of bitarrays.

# BBFquery.py

The code contains class BBFquery(), which also imports bitarray and mmh3 package for bit-vector arrays and hash functions, respectively. This is very similar to BFbuild.py. The input queries need to go through the same hash function as in the BBFbuild() class in order to check if the queries are present in the set. The first hash function will pick the block, and the rest of the hash functions will pick the indices within that block. If one of the hash functions returns ‘0,’ then the class will return False, which means that the query is not present in the bloom filter set. At the end of the standard out, the program will also show how many queries are in the set (True) and how many are not in the set. 

## Usage of ‘query’

The ‘query’ argument will take the `output.txt` from ‘build’ command-line argument as an input and output the result of issuing each of the queries to standard out. 
The required options for the command-line argument are:

```
--input= or -i
--query= or -q
```

The input (--input= or -i) text file should be the output from the ‘build,’ and the query (--query= or -q) text file is provided by the user (just the list of random query strings that might or might not be in the set). The example of the usage is:

```
$ python blockedbf.py query -i <output from ‘build’> -q <query input>
```

*`-h` or `--help` option will list the options and their descriptions*

## query1.txt

There are no query keys present in the original set.

## query2.txt

There are 50% of query keys that are present in the original set.

## query3.txt

There are 100% of query keys that are present in the original set.

*The query files are also same as the standard Bloom Filter*

# Difficult part

The most difficult part of the project overall was to design the plot. I had so many different numbers of queries, and therefore making many combinations. I had to figure out how to efficiently plot the generated data without creating multiple similar graphs. I used stacked bar plots to visualize empirical false positive rates, and line plots with different colors to show the time cost for the query. 
