# string.equals(integer) Writeup

### Prompt

> Someone gave me two functions to convert strings into integers. I converted some strings to the integers and noted them down. Can you help me converting the concatenation of those strings in the order mentioned in the file hashes.txt into integers?

> The answer for this is the multiplication of output of both the functions for the concatenated string. (Wrap the number around flag{})

File: [hash.zip](hash.zip)

### Solution

The problem, after a couple read-throughs and looking at the files provided, makes clear that to generate [hashes.txt](hash/hashes.txt), the creator ran the provided [chall.py](hash/chall.py). This program includes two hash functions with different moduluses, as well as some driver code. 

The best approach (we could come up with) to crack this (the same way as one would approach cracking a real hash) is to use the hash function to generate a dictionary of results based on all (or many -- in this case all) inputs as possible, and then use the dictionary to look up the hash and recieve (hopefully) the source. 

We implemented that in [dict.py](dict.py), and after several iterations, we were able to derive a hash dictionary. This dictionary contains all the hashes (for both algorithms) for every unique set of 1 to 100 characters from input files 0-19 (I concatenate them together, and while it is less efficient, it has more values in the dict, in case the problem needs those). 

Then, we swap the keys for values and create a new dictionary. This one, we use to look up each hash of the 10000 in [hashes.txt](hash/hashes.txt), and we get a list of "words" (not phonetic words, character sequences). As the problem instructs, we concatenate them, creating a long string. We get the `func1()` and `func2()` hashes of that string, and multiply them together to get:

```
flag{82806233047447860}
```

~ Lyell Read, Phillip Mestas, Lance Roy