# Vault Writeup

### Prompt

> We locked our secret box, You can directly ping the bot (@Vault #8895 ) using "start" to get the secret but we don't know the door code we used random() also we used sleep(10).

> shift register...

> Author : Harsh and warlock_rootx

> Hint: if pin in user_input(): #Good Stuff...

### Solution

This problem (and especially the hint) make clear what we have to do. We need to provide the discord bot with as many possible passcodes as we can for the suggested charset and length as possible... now, discord makes this hard, as messages are limited to 2000 characters. The bot asks for these passcodes:

```
[0, 1]				l=7
[4, 5, 6] 			l=6
[5, 6, 7, 8, 9] 	l=4
[1, 2, 3, 4] 		l=5
[0, 1, 2, 5, 8, 9] 	l=4
[0, 1] 				l=11
```

Despite sometimes having to choose as little as 1/12 of the total passcode wordlist size, I was able to get the challenge during the ctf with a 'bruteforce' tactic. The strings that I sent are in [strings-bruteforce.txt](strings-bruteforce.txt), and they worked in a couple of tries (the odds were better than they may seem, as overlapping passcodes count too). Some passcode sets (like that of the last problem). I made these strings with python itertools:

```python
import itertools
passcode_list = list(itertools.product(charset, repeat=length))
print(''.join([''.join(y) for y in passcode_list]))
```

After the CTF, though, I was nagged by the fact that I could improve on this... I therefore made a partial superstring program to make the strings shorter, and include more possible passcodes per message to the bot. It is [here](superstring.py), and it creates [these passcode lists](strings-partial-superstring.txt). All apart from the last one will be 100% reliable, as I had to shave 200 characters off the last one. My superstring algorithm is lazily made, and not perfect, so there exists a case where one could compose strings that would contain all passcodes for all challenges proposed by the bot. 

All in all a fun quick chall! 

```
IJCTF{0p3n3d_d3_bru1jn_v4ul75}
```

~ Lyell Read