from PIL import Image
import os
from Crypto.Util.number import long_to_bytes

outimage = []

print("Reading")

for file in os.listdir("images/"):
	in_image = Image.open("images/" + file, 'r')
	pixel = list(in_image.getdata())
	outimage.append([long_to_bytes(int(file.replace('.jpg', ''))).decode("utf-8") , pixel[0]])

print("Changing Index")

for x in outimage:
	x[0] = int(x[0].split(' ')[0]) * 1000 + int(x[0].split(' ')[1])

print("Sorting")

outimage.sort(key=lambda x : x[0])

print ("Cleaning Up")

outimage_sorted = [x[1] for x in outimage]

print("Making Image")

im2 = Image.new('RGB', (300, 300))
im2.putdata(outimage_sorted)
im2.save("out.png")