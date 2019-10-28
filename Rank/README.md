bitVectorRank.py will import RankSupport.py and BitVector.py (https://github.com/jeetsukumaran/supertramp/blob/master/supertramp/BitVector.py) to implement rank_indexAt().

# bitVectorRank.py

This python code will generate a random-sized random bit-vector array (range from 1000 to 100000) using BitVector.py
Then it will call RankSupport.py with the randomly generated bit-vector and the size of the bit-vector as its parameters.

This process will be repeated 1000 times to generate the plot of the assignment (x-axis: bit-vector size, y-axis: time cost)

# RankSupport.py

This code contains class RankSupport(), which accepts bit-vector array and its size that are generated in bitVectorRank.py as parameters.
With its size, it can calculate the sizes of superblocks and blocks, and number of superblocks, blocks and block types. 
I also made a separate function (countBits) to count bits from one index to another, because count_bits() from BitVector returns the counts of 1's in the whole bit-vector array (with no specified range within the array).

rank_s() function will accept bit-vector array and return an array with the ranks at the beginning of each superblock.
rank_b() function will also accept bit-vector array and return a dictionary that contains the ranks for each block within the corresponding superblock. Therefore the key of this outcome dictionary will be the index of the superblock, and the values (in array) will be the ranks at the beginning of each block within the superblock.
rank_p() function will also accept bit-vector array and return a dictionary that contains every possible block types. The key of this outcome dictionary will be the possible block type, and the values (in array) will be the rank in each position within the block type.
Finally, rank_indexAt() function will accept bit-vector and the target index and search through the array and dictionaries created from rank_s(), rank_b(), and rank_p() to add the ranks from each function to get the final rank of that index.
I made a separate function, rank_indexAtforSelect() for SelectSupport.py (explained in README.md of SelectSupport.py)

# Difficult part
The most difficult part of this task was to write a class function on Python. I am somewhat new to Python and had never used class implementation. I googled some basics of Python class and applied to current assignment, but I am not sure if this is the right (or conventional) format. I would love to learn more about Python or C++. Another hardship was to figure out which data type I should use for rank_b() and rank_p(). rank_s() was simple enough to use an array, but for rank_b() and rank_p() (especially rank_p()), I figured that it is too complicated for me to use just array because they depend on the previous outcomes (rank_b() depends on rank_s() and rank_p() depends on rank_b()).

