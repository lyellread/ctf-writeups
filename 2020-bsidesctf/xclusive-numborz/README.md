# BSidesPDX Xclusive Numborz

### Prompt

> Category: Over The Air
> 290 Points
> 8 Solves

I was watching my regularly scheduled state sponsored programming when I got some strange interference. It sounded like a little girl was talking to me but I couldn't understand what she was saying. Can you figure it out? There's no space for mistakes, and no room for questions.

[twitch.tv/over_the_air](https://twitch.tv/over_the_air)

Author(s): 0xdade & fdcarl

### Solution

The first challenge was easy, but this one is a little trickier. We are told to listen to the segment where a "little girl" talks, and the name implies that we will be doing some XOR.

Beginning at [8:24 in the recording of the stream](https://youtu.be/_QgPMyRBBKM?t=504), We hear a child's voice say "you're all gonna die down here", we see a creepy plague doctor image moving around in the background, and a child's voice speaking letters and numbers in the foreground, finishing with the phrase "are you my mommy" repeated twice. At first the letters and numbers that the child spoke sounded to me like:

```
23210C1D0A063D3D3I1419054A3E1C10140D461F0A321C1DIE4D0A2DI1261G1DIE141EIC011G4A120F
```

This string uses charset `['0', '1', '2', '3', '4', '5', '6', '9', 'A', 'C', 'D', 'E', 'F', 'G', 'I']`, which is a little odd.

However on closer inspection, and after consulting my teammates, the string was determined to be:

```
23210C1D0A063D3D351419054A3E1C10140D461F0A321C1D5E4D0A2D51261B1D5E141E5C011B4A120F
```

This is because I misheard 'B' as 'G', and '5' as 'I', and I did not pick up on the fact that the charset I had was hex with two wrong characters. 

From that string, we can guess that it might be a flag, which has format `BSidesPDX{}`, and infer what the XOR key should start with (we used the assumption that `a^b=c` and `a^c=b`.

```
String : 23 21 0C 1D 0A 06 3D 3D 35 14 ... 
Key    : ?  ?  ?  ?  ?  ?  ?  ?  ?  ?  ...
Output : 42 53 69 64 65 73 50 44 58 7b 
(Ascii): B  S  i  d  e  s  P  D  X  {

Key    : 61 72 65 79 6f 75 6d 79 6d 6f
(Ascii): a  r  e  y  o  u  m  y  m  o
```

That key looks an aweful lot like "areyoumymommy", which is the key for the XOR decryption ("areyoumymommyareyoumymomm"...).

```
BSidesPDX{th3_numb3rs_sp34k_4_th3ms3lv3s}
```

~Lyell