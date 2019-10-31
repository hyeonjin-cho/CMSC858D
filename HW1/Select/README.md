bitVectorSelect.py and SelectSupport.py import RankSupport.py and BitVector.py (https://github.com/jeetsukumaran/supertramp/blob/master/supertramp/BitVector.py) to implement select_rankOf().

# bitVectorSelect.py

This python code will generate a random-sized random bit-vector array (range from 1000 to 100000) using BitVector.py Then it will call SelectSupport.py with the randomly generated bit-vector and the size of the bit-vector as its parameters.

This process will be repeated 500 times to generate the plot of the assignment (x-axis: bit-vector size, y-axis: time cost)

# SelectSupport.py

This code contains class SelectSupport(), which accepts bit-vector array and its size that are generated in bitVectorSelect.py as parameters. With its size, it can calculate the sizes of superblocks and blocks, and number of superblocks, blocks and block types. I also made a separate function (countBits) to count bits from one index to another, because count_bits() from BitVector returns the counts of 1's in the whole bit-vector array (with no specified range within the array). Since select function should use rank function, this class will import RankSupport.py class. 

callRankSupport() function will accept bit-vector array and its size to generate rank_s(), rank_b(), and rank_p() tables (See RankSupport.py for the explanations). 
getRank() function will recursively accept bit-vector array, its size and index count (starting at 0 for the first recursive run) as its parameters and return the index of the selected rank. 
select_rankOf() function will accept bit-vector array and target rank (the rank you are interested in) as its parameters and call getRank() function. It will also give an error message when the user gives rank that is out of range. 

# Difficult part

This task was relatively easier compared to RankSupport.py. It only took me less than a day to figure out select_rankOf(), when I had rank_indexAt(). The most difficult part was that the regular rank_indexAt() would not work with select because I wrote the code to give an error message when the index from the user is not 1. Therefore, I made a rank_indexAt() derivative (called rank_indexAtforSelect()), which will give the rank at the index even if the index is not 1. Also, generating the random-sized bit-vector and implementing select_rankOf() of that bit-vector took even more time than rank_indexAt() of RankSupport.py, so I only generated 500 random-sized bit-vector, instead of 1000 which I did for RankSupport.py. Another difficulty that I encountered during this programming was figuring out the time complexity. I expected to have O(logn) time complexity, however, the graph gave more linear-like graph. At first, the time it took for the largest bit-vector was around 0.5 seconds (Figure 1). I found out that I do not actually need to call for bit-vector every time, so as a result successfully reduced by 1/5 (Figure 2), by just removing a line of code that called the bit-vector. However, the graph still looks more linear than logarithmic.

# 500_random.pdf

This pdf file depicts how much time SelectSupport.py took to get the index of the target rank. X-axis is size of bit-vector, randomly generated from size 1000 to 100000. I simply took difference of the time right before select_rankOf() and right after select_rankOf() to get the timeCost. Since select_rankOf() calls another function, getRank(), which is a recursive function, the time cost will be bigger than rank_indexAt(). The time complexity for select_rankOf() will be O(logn), but the pdf file does not support this. This might be because of the time consumed when calling bv during rank_indexAt().
*I only uploaded Figure 2 in the GitHub, but Figure 1 is also presented on ELMS submission.*
*R programming was used to generate the plot.*
