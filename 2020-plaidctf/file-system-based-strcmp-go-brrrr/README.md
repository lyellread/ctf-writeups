# File System Based Strcmp Go Brrr - 150pts

## Prompt

> strcmp go brrrr

Files: [strcmp.tar.gz](strcmp.tar.gz)

## Solution

This challenge revolved around [a fat32 file system image](strcmp.fat32). After mounting the image we saw an endless tree of recursive directories full of the alphabet and some other characters. Each directory contained an empty file with a name indicating that you had not found the flag, such as `TROLOL` or `NOFLAG4U`.

We quickly guessed that the directory structure was a file system based trie and that the flag would then be a path through the filesystem, likely to a zero byte file with a congradulatory name. Looking through a strings dump of the filesystem we saw that the file we were looking for was called `MATCH`. Unfortunately the file system recursed extremely deep so any effort to find the flag with a basic find command failed. 

Finally we discovered that there were many more directories in the fs than were possible given its size. This meant that the directories were likely hard linked. After making this discovery we edited our find script to track and ignore directories with inode values that we had already visited.

We then used [a python script](solve.py) to find our flag in the directory 

```
SPACE/SPACE/SPACE/!/SPACE/SPACE/SPACE/!/!/SPACE/SPACE/!/!/SPACE/!/SPACE/!/#/$/#/#/SPACE/#/%/$/#/!/!/#/!/$/%/#/#/#/$/%/&/'/$/%/$/%/%/#/$/&/(/%/&/&/&/)/$/'/'/(/)/&/'/(/%/&/'/$/(/)/'/&/-/-/(/-/)/'/0/0/(/%/-/1/1/)/0/-/'/1/2/&/3/$/(/(/%/)/0/)/0/'/-/2/1/-/1/3/)/(/2/)/3/&/4/4/2/2/5/4/6/'/5/6/7/3/4/-/(/0/5/1/8/6/2/3/4/)/-/3/7/4/5/0/0/0/8/5/1/9/1/9/6/6/7/8/2/2/5/9/@/-/3/7/@/7/@/4/8/8/9/6/7/3/5/0/8/6/A/1/A/9/@/9/2/7/4/A/8/5/A/B/6/B/B/@/1/@/C/2/3/3/D/9/A/C/7/A/@/4/B/C/D/B/C/5/E/B/D/D/A/E/6/E/4/B/F/5/G/E/7/F/G/8/9/F/8/G/@/6/9/C/A/@/F/C/7/G/B/H/H/H/I/D/J/C/I/I/8/A/C/D/J/H/K/D/D/9/E/F/L/E/B/F/K/E/L/G/@/G/I/H/E/C/I/J/M/K/N/J/A/L/F/O/G/J/F/D/H/G/E/K/H/I/H/P/SPACE/B/L/M/Q/I/J/M/K/N/F/K/C/R/L/M/I/S/J/O/K/L/G/H/M/I/M/N/N/L/N/N/O/M/J/J/P/SPACE/K/K/O/T/O/P/!/N/P/SPACE/L/L/D/P/SPACE/E/U/Q/O/Q/V/Q/R/S/R/P/!/S/W/Q/X/F/O/M/T/G/H/Y/P/SPACE/N/T/Q/M/I/R/R/S/U/U/R/Z/J/S/K/^/T/L/V/M/N/T/N/W/X/U/Y/Z/_/O/`/U/V/O/V/^/V/{/}/W/_/W/X/P/$/P/!/O/Y/W/`/}/S/Z/P/C/P/C/P/C/P/P/C/T/F/P/C/T/F/{/P/P/C/T/F/P/C/T/F/P/C/T/F/{/W/H/A/T/_/I/N/_/T/A/R/N/A/T/I/O/N/_/I/S/_/T/H/1/S/_/F/I/L/E/S/Y/S/T/E/M/!/}
```

This flag directory ends in `..../P/C/T/F/{/W/H/A/T/_/I/N/_/T/A/R/N/A/T/I/O/N/_/I/S/_/T/H/1/S/_/F/I/L/E/S/Y/S/T/E/M/!/}`, which contains our flag:

```
PCTF{WHAT_IN_TARNATION_IS_TH1S_FILESYSTEM!}
```

~ REK, Phillip Mestas, Lance Roy, Andrew Quach, Lyell Read