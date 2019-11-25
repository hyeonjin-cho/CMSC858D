bf.py, BFbuild.py and BFquery.py import bitarray.py (https://pypi.org/project/bitarray/) and mmh3 (https://pypi.org/project/mmh3/) 

# bf.py

This python code will read an input text file (testKey.txt) to generate Bloom Filter bitarray. There are two command-line arguments for this program. One is ‘build,’ which will build the Bloom Filter, and the other is ‘query,’ which will issue each of the queries in the query file. The specifics of the usage for each command-line arguments are described below. 

# BFbuild.py

The code contains class BFbuild(), which imports bitarray and mmh3 package for bit-vector arrays and hash functions, respectively. bf.py ‘build’ argument will pass desired false positive rate and number of unique keys for bitarray size (bloom filter size, m) and number of hash function (k) calculations. After setting the size of the bitarray (initially the bitarray is set to all ‘0’), the program will run the hash function k times. Since the value from the hash function will be much bigger than the size of the bloom filter, the program will take the hash function modulo the bloom filter size. The result from the modulo operation will be the index of the bitarray. For example, let’s say m = 70 and the input key ‘xmnwmosqgo’ is put into the first hash function from mmh3, the value is 2113109185. Then 2113109185 % 70 = 5 is the index for this input key. Since we are taking the modulo of 70, the range of the value will always be from 0 to 69. 

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
$ python bf.py build -k <test key input> -f <desired false positive rate> -n <num. of unique keys> -o <output>
```

*`-h` or `--help` option will list the options and their descriptions*

## testKey.txt

This text file contains input key for bloom filter construction. It is randomly generated using online tool (http://www.unit-conversion.info/texttools/random-string-generator/). I only used first 9 alphabets (all lowercase) to generate 10,000 strings with length 5. The number of unique keys is 9195.

## Example

```
$ python bf.py build -k testKey.txt -f 0.1 -n 9195 -o output.txt
```
The output.txt will look like this:
```
0.1
9195
44068
4
bitarray(‘0000101110… 1110111101’)
```
The numbers in the output.txt are fpr, numKeys, size of bloom filter, number of hash functions, and the bitarray.

# BFquery.py

The code contains class BFquery(), which also imports bitarray and mmh3 package for bit-vector arrays and hash functions, respectively. This is very similar to BFbuild.py. The input queries need to go through the same hash function as in the Bfbuild() class in order to check if the queries are present in the set. If one of the hash function returns ‘0,’ then the class will return False, which means that the query is not present in the bloom filter set. At the end of the standard out, the program will also show how many queries are in the set (True) and how many are not in the set. 

## Usage of ‘query’

The ‘query’ argument will take the `output.txt` from ‘build’ command-line argument as an input and output the result of issuing each of the queries to standard out. 
The required options for the command-line argument are:

```
--input= or -i
--query= or -q
```

The input (--input= or -i) text file should be the output from the ‘build,’ and the query (--query= or -q) text file is provided by the user (just the list of random query strings that might or might not be in the set). The example of the usage is:

```
$ python bf.py query -i <output from ‘build’> -q <query input>
```

*`-h` or `--help` option will list the options and their descriptions*

## query1.txt

There are no query keys present in the original set.

## query2.txt

There are 50% of query keys that are present in the original set.

## query3.txt

There are 100% of query keys that are present in the original set.

# Difficult part

The most difficult part I faced as I write the implementation was that the empirical false positive rate was very high than the desired false positive rate. I thought it was because of the size of my bloom filter, so I tried increasing the size by 50%. However, after talking with Dr. Patro, this could be easily fixed by changing math.log2 to math.log (natural log for python math package). Another difficult part was to efficiently visualize the results. Since I was not sure how many input keys to use to build a bloom filter, I tried with a range of input keys (from 500 to 10,000, in GitHub I only uploaded 10,000 input keys). I only used query1.txt and query2.txt result to draw the plots, because query3.txt contains the queries that all are present in the original set. 
