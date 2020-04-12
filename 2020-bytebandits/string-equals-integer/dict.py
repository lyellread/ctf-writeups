import os, random

def func1(s):
    h = 0
    for i in range(len(s)):
        h += (ord(s[i]) - 96) * pow(31, i, int(1e9 + 7))
        h %= int(1e9 + 7)
    return h


def func2(s):
    h = 0
    for i in range(len(s)):
        h += (ord(s[i]) - 96) * pow(31, i, int(1e9 + 9))
        h %= int(1e9 + 9)
    return h

dictionary = {}

def chunkgen(d, s):
	out = []
	# for i in range(0, len(s)-99):
	# 	for x in range(1,101):
	for i in range(0, len(s)):
		for x in range(1,min(101, len(s) - i) + 1):
		
			c = s[i:i+x]
			if c not in d:
				#print("Adding to Dictionary")
				d[c] = str(func1(c)) + ' ' +  str(func2(c))

	# 		out.append(s[i:i+x])
	# return out

aft = ""
for file in os.listdir("./hash/a/"):
	print("New File")
	with open("./hash/a/" + file, 'r') as f:
		aft += f.read()
		f.close()

print("All:", aft)

print("Generate Chunks, Make Dictionary")
generate_chunks = chunkgen(dictionary, aft)

out = []

dictionary2 = {}

print("Flipping Dictionary")
for key, value in dictionary.items():
	dictionary2[value] = key

print("Writing to file")
with open("./dict", 'w') as f:
	f.write(str(dictionary2))
	f.close()

print("Reversing hashes")
with open("./hash/hashes.txt", 'r') as f:
	hashed = [x.replace('\n', '') for x in f.readlines()]
	f.close()

for x in hashed:
	print("Handling hash:", x)
	c = dictionary2[x]
	out.append(c)
	#print("Found:", out)

print("Concatenating")
o = ''
for x in out:
	o += x

print("Hashing")
f1 = func1(o)
f2 = func2(o)

print("Result", f1 * f2)