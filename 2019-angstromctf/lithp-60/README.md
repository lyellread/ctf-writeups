# Lithp Writeup - 60 Points

### Prompt 

My friend gave me [this](lithp.lisp) program but I couldn't understand what he was saying - what was he trying to tell me?

Author: fireholder

### Solution

First things first, let's open that lisp program . . . It actually is lisp. . . oh god what have I just gotten into?

The first lines were most important in solving this challenge the way I did it. It reads:
```lisp
(defparameter *encrypted* '(8930 15006 8930 10302 11772 13806 13340 11556 12432 13340 10712 10100 11556 12432 9312 10712 10100 10100 8930 10920 8930 5256 9312 9702 8930 10712 15500 9312))
(defparameter *flag* '(redacted))
(defparameter *reorder* '(19 4 14 3 10 17 24 22 8 2 5 11 7 26 0 25 18 6 21 23 9 13 16 1 12 15 27 20))
```	
Well, then. Given that I do not want to dig into the lisp program further than I have to (lest I end up depressed), let's try to make some sense just based on those variables. With quite a bit of certainty, it appears that reorder is as it is named - an array of indexes that will reorder something. My guess is that it is applied like this:
```
flag: 97 99 116 102 123 ... 125
encrypt flag
for entry[i] in encrypted_flag: place that element at output[reorder[i]]
```	
Now we need to try to unjumble this. I wrote up this mess to do that:
```python
positions = [19, 4, 14, 3, 10, 17, 24, 22, 8, 2, 5, 11, 7, 26, 0, 25, 18, 6, 21, 23, 9, 13, 16, 1, 12, 15, 27, 20]
values = [8930, 15006, 8930, 10302, 11772, 13806, 13340, 11556, 12432, 13340, 10712, 10100, 11556, 12432, 9312, 10712, 10100, 10100, 8930, 10920, 8930, 5256, 9312, 9702, 8930, 10712, 15500, 9312]
output = []

for item in range (0, max(positions) + 1):
	index = positions.index(item) #get the index in values of element number item
	output.append(values[index])  #place that at the end of the output list 

print (output)
```
... and ran it:
```
$python3 ./undo_reorder.py
[9312, 9702, 13340, 10302, 15006, 10712, 10100, 11556, 12432, 8930, 11772, 10100, 8930, 5256, 8930, 10712, 9312, 13806, 10100, 8930, 9312, 8930, 11556, 10920, 13340, 10712, 12432, 15500]
```
Apparently, that should be in the right order. Let's think about it with ASCII on the mind, we should have 'actf{...}'. Looks about right with two very similar values in the spots where we would expect '{' and '}'...

But those aren't ASCII! yeah, but they are transformations of ascii values. It cannot be a scalar that is added to the ASCII values of the respective flag characters, as the '{' and '}' values would have to be 2 apart ('{' = 123, '}' = 125). There could be a scalar value that all the ASCII codes are multiplied by. Let's check that first value, 9312, which should be related to ASCII 97 ('a'):
```
>>>9312/97
96
```	
...interesting. Let's try another: 15006 which should correspond to '{' = 123:
```
>>>15006/123
122
```	
OK. So the algorithm to encrypt the flag is just:
```python
for x in flag: 
	code = ascii value of x
	encrypted_value = code * (code-1)
```	
Now we can complete the script:
```python
sorted = [9312, 9702, 13340, 10302, 15006, 10712, 10100, 11556, 12432, 8930, 11772, 10100, 8930, 5256, 8930, 10712, 9312, 13806, 10100, 8930, 9312, 8930, 11556, 10920, 13340, 10712, 12432, 15500]

letters = []
decoded = []
solved = []

for ascii in range (0, 128):
	letters.append(ascii*(ascii-1))			#create an array of all ascii values such that the index is the original value, and the value at that index is the encoded value.

for x in sorted:
	if x in letters:
		decoded.append(letters.index(x))	#create a decoded array of values

for x in decoded:
	solved.append(chr(x))				#convert to chars

print (''.join(solved))					#print that flag
```	
These two scrips together make up [decode_lithp.py](https://github.com/lyellread/ctf-writeups/blob/master/angstromctf-2019/lithp-60/decode_lithp.py).
```
$python3 ./undo_encrypt.py
actf{help_me_I_have_a_lithp}
```
Nice!

~Lyell Read
