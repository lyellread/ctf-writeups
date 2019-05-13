# Restricted Puzzle Writeup

### Solution

The only file given is a GIF image, named [`redacted-puzzle.gif`](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/redacted-puzzle.gif). We must first inspect it:

```bash
$ exiftool redacted-puzzle.gif
ExifTool Version Number         : 10.80
File Name                       : redacted-puzzle.gif
Directory                       : .
File Size                       : 78 kB
File Modification Date/Time     : 2019:05:10 17:05:42-07:00
File Access Date/Time           : 2019:05:10 17:05:42-07:00
File Inode Change Date/Time     : 2019:05:10 17:26:26-07:00
File Permissions                : rwxrwxrwx
File Type                       : GIF
File Type Extension             : gif
MIME Type                       : image/gif
GIF Version                     : 89a
Image Width                     : 1280
Image Height                    : 720
Has Color Map                   : Yes
Color Resolution Depth          : 3
Bits Per Pixel                  : 2
Background Color                : 3
Animation Iterations            : Infinite
Frame Count                     : 35
Duration                        : 8.75 s
Image Size                      : 1280x720
Megapixels                      : 0.922
```

OK. We know that this is likely a GIF with 35 frames. Let's try opening it:

![Image](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/open-in-image-viewer.JPG)

Let's gather some more information about this GIF:

```bash
$identify -verbose redacted-puzzle.gif

 . . .

  Colormap:
         0: (  0,  0,  0,255) #000000FF graya(0,1)
         1: (  0,  0,  0,255) #000000FF graya(0,1)
         2: (  0,  0,  0,255) #000000FF graya(0,1)
         3: (255,255,255,  0) #FFFFFF00 graya(255,0)

 . . . 

```

That is a bit of a weird color map... Those should correspond with different colors. Let's open this image in [gimp](https://www.gimp.org/). We use the `Open as Layers` option to get each frame as an individual layer.

![Image](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/layers.JPG)

Much layers. Next, we gotta fix that color mapping issue. `Colors>Map>Set Color Map` and choose `Pallete>Ega`:

![Image](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/map_1.JPG)

Well, we know what the flag's alphabet will be. Then, after looking at each slide . . . 

![Image](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/c2a_1.JPG)

We determined it best to remove the black backgrounds on each. One by one.

![Image](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/c2a_2.JPG)

Now we can see them all overlapping. They form some sort of circle:

![Image](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/all_transparent.JPG)

Let's examine only a couple...

![Image](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/octagon_2.JPG)

That is intresting. Going off a hunch, we decided to build sets of binary digits representing if the vertex of a frame was where one of the verticies of the overall 'octagon', using dots in the background:

![Image](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/dots.JPG)

![Image](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/example_binary.JPG)

As we repeated that for each layer, the shapes' verticies started to 'rotate', or 'drift' (thus why when all overlayed, they formed a circle, not octagon). We decided to track the movment and adjust the background dots. We generated the 'bytes':

```python

verticies = ['10001100', '01100011', '11100100', '01000110', '10000101', '00111101', '01000010', '10011000', '11100000',
             '11110100', '10000000', '00101101', '01110010', '00011100', '00001000', '10100101', '11010111', '01101110',
             '10100110', '10010001', '10111100', '10000100', '10000001', '10111001', '11010100', '00111011', '11001110',
             '11110010', '00011110', '10011101', '11001001', '11000111', '01100101', '00011110', '10011111']
```

Now comes the challenge of making sense of those. We know that the first three should be the same (which they arent) because flags start with `OOO...`. A pattern appears when you concattenate the first couple 'bytes':

`100011000110001....`

That looks to be three identical 5- bit numbers. Concattenating all of the `verticies` and splitting them by 5's yields:

```python

cintuplets = ['10001', '10001', '10001', '11110', '01000', '10001', '10100', '00101', '00111', '10101', '00001',
			  '01001', '10001', '11000', '00111', '10100', '10000', '00000', '10110', '10111', '00100', '00111',
			  '00000', '01000', '10100', '10111', '01011', '10110', '11101', '01001', '10100', '10001', '10111', 
			  '10010', '00010', '01000', '00011', '01110', '01110', '10100', '00111', '01111', '00111', '01111', 
			  '00100', '00111', '10100', '11101', '11001', '00111', '00011', '10110', '01010', '00111', '10100', 
			  '11111']
```

Those first couple convert to be 17 in decimal. Coincidentally, at index 17 of our alphabet is the letter 'O'. 

Note that in [redacted-puzzle-solve.py](https://github.com/lyellread/ctf-writeups/blob/master/dcquals2019/redacted-puzzle-writeup/redacted-puzzle-solve.py) we exclude the location that you started forming the bits for each byte of `verticies` from on the octagon.

```
OOO{FORCES-GOVERN+TUBE+FRUIT_GROUP=FALLREMEMBER_WEATHER}
```
