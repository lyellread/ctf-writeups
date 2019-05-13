#!/usr/bin/python

positions = [19, 4, 14, 3, 10, 17, 24, 22, 8, 2, 5, 11, 7, 26, 0, 25, 18, 6, 21, 23, 9, 13, 16, 1, 12, 15, 27, 20]
values = [8930, 15006, 8930, 10302, 11772, 13806, 13340, 11556, 12432, 13340, 10712, 10100, 11556, 12432, 9312, 10712, 10100, 10100, 8930, 10920, 8930, 5256, 9312, 9702, 8930, 10712, 15500, 9312]
sorted = []

for item in range (0, max(positions) + 1):
	index = positions.index(item)
	sorted.append(values[index])

#sorted = [9312, 9702, 13340, 10302, 15006, 10712, 10100, 11556, 12432, 8930, 11772, 10100, 8930, 5256, 8930, 10712, 9312, 13806, 10100, 8930, 9312, 8930, 11556, 10920, 13340, 10712, 12432, 15500]

letters = []
decoded = []
solved = []

for ascii in range (0, 128):
	letters.append(ascii*(ascii-1))
	
for x in sorted:
	if x in letters:
		decoded.append(letters.index(x))

for x in decoded:
	solved.append(chr(x))

print (''.join(solved))
