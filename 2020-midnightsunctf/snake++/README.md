# Snake++

141 points

### Prompt

> Snake Oil Co. has invented a special programming language to play their new and improved version of Snake. Beat the game to get the flag.
settings Service: `nc snakeplusplus-01.play.midnightsunctf.se 55555`

### Solution

When I first connected to the remote server, I was presented with a menu, detailing 3 options: Play in player mode, play in computer mode, or exit. The rules detail that a score of 42 will grant you a flag, so I first tried in player mode (where I direct the snake).

- `A` is a good apple: it grows the snake 1 in length
- `B` is a bad apple, it shrinks the snake in length. Best shoot these

The snake is controlled with:

- `L` - will advance the snake one place ***then*** turn the direction 90 degrees left.
- `R` - will advance the snake one place ***then*** turn the direction 90 degrees right.
- `' '` (space) will "shoot" in the direction the snake is pointed, until it hits either `A` (which it will delete), `B`, which it will delete, or your snake, or the wall. Note: you don't die if you shoot yourself. After shooting, the snake moves forward one square
- `''` (enter), which will advance the snake 1 in the direction it points.

When I played in player mode, I noticed no warning that no flag would be given for a win in player mode, so I figured if I could endure the tedious game (the move before turn, paired with me being bad at rights and lefts made this angering at best), I would get flag... easy, right? Two hours later, I finally reached a score of 42, and the game did not give me a flag >:(.

Now to computerize it. The language description for Snake++ is presented in [lang-desc.txt](lang-desc.txt). 

Our game plan now becomes the writing of a function in Snake++ that can choose the next move based on board state. We implemented it in parts:

- [driver.py](driver.py) - supplies [snake.ai](snake.ai) to server, and runs in while loop, detecting flag if won.
- [snake.ai](snake.ai) - a misnomer, as this is really quite a dumb function (and not ***at all*** optimized, which we were too tired to see at the time). This is the Snake++ program/function that determines the move to make. This function encompasses:
	- A hamiltonian cycle through the map, stored to RAM. [hampath.txt](hampath.txt) shows this - start in left bottom corner facing right, and the move in your cell is what to submit to stay on hampath.
	- Logic to determine what to do based on cycle, apple type...

[snake.ai](snake.ai) loads the hamiltonian path/cycle into RAM if it is not there already (we could optimize this by not writing all the `F`'s). Then:

- If we are on a turn in the hampath, we must turn
- If there is a `B` near, return shoot (`' '`)
- Else, move forward.

> Note: `snake.ai` requires the starting (random) position to be the same direction of the hampath at that spot, so probability decrees that it works 1/4 tries.

I know, we are all CS majors, and while you might expect a better solution from us, we are also masters of minimal effort. 

So, this scrip ***barely*** works... We ran it in a loop, one run at a time (as to keep the server as fast as possible), and consistently got scores of 30-39 (there's a 90-sec timeout for computer mode). Then, on a lucky run, we got a score of 42. 

```
midnight{Forbidden_fruit_is_tasty}
```

~ Lyell Read, Phillip Mestas, Athos