# ALCAPONE Writeup

### Prompt

Eliot Ness is the lead on taking down Al Capone. He has gained access to Capone's personal computer but being the good detective he is, he got the disk image of the computer rather than look through the actual computer. Can you help Ness out and find any information to take down the mob boss?

(hint: Al Capone knew his computer was going to be taken soon, so he deleted all important data to ensure no one could see it. Little did he know that Ness was smarter than him.)

Direct Download link: https://tamuctf.com/themes/core/static/img/WindowsXP.img.xz

Files: [WindowsXP.img](WindowsXP.img)

### Strings Solution

OK, kinda feel like a dumbass for spending the effort and time to install Autopsy and perform proper windows forensics on this image, when I could have just done: 

```bash
strings WindowsXP.img | grep 'gigem{'
oigigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}khsutrghsiserg
```

Next time, maybe check strings first?

### Forensic Solution

Open this in [Autopsy](https://www.sleuthkit.org/autopsy/), and let it rpepare the files. Then, given that the prompt says that all the important (read: flag-containing) stuff has been deleted, we will pull all the `flag??.txt` from the trash bin (and I also pulled the ones from Administrator's Desktop), and export them. You get [flags.zip](flags.zip). Once extracted, it is as simple as:

```bash
unzip flags.zip
cd flags
for x in ./*; do strings $x | grep 'gigem{'; done 
oigigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}khsutrghsiserg
oigigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}khsutrghsiserg
```

Um... not exactly the challenge I was expecting but cool :). 

```
gigem{Ch4Nn3l_1Nn3R_3l10t_N3$$}
```

~Lyell Read
