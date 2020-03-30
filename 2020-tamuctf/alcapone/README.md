# ALCAPONE Writeup

### Prompt

Eliot Ness is the lead on taking down Al Capone. He has gained access to Capone's personal computer but being the good detective he is, he got the disk image of the computer rather than look through the actual computer. Can you help Ness out and find any information to take down the mob boss?

(hint: Al Capone knew his computer was going to be taken soon, so he deleted all important data to ensure no one could see it. Little did he know that Ness was smarter than him.)

Direct Download link: https://tamuctf.com/themes/core/static/img/WindowsXP.img.xz

### Unintended Solution

Um... `strings`? 

```
strings WindowsXP.img | grep 'gigem{'
oigigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}khsutrghsiserg
oigigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}khsutrghsiserg
oigigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}khsutrghsiserg
gigem{Ch4Nn3l_1nN3r_3Li0t_N3$$}
```

### [Possibly] Intended Solution

I installed [Autopsy](https://www.autopsy.com/), and opened the image file. Given the hint about the files having be deleted, we can look through the recycling bin and extract all the `flag??.txt` files (and those from the Administrator's Desktop) to [flags.zip](flags.zip). Then:

```
unzip flags.txt
cd flags
for x in ./*; do strings $x | grep 'gigem{'; done
oigigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}khsutrghsiserg
oigigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}khsutrghsiserg
```

```
gigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}
```

~Lyell Read
