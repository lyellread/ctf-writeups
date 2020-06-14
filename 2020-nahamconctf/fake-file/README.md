# Fake File

100 points

### Prompt

> Wait... where is the flag?

> Connect here:
> `nc jh2i.com 50026`

### Solution

Let's `nc` to that server and see what's up:

```bash
$ nc jh2i.com 50026

bash: cannot set terminal process group (1): Inappropriate ioctl for device
bash: no job control in this shell
user@host:/home/user$ ls -lah
ls -lah
total 12K
dr-xr-xr-x 1 nobody nogroup 4.0K Jun 12 17:10 .
drwxr-xr-x 1 user   user    4.0K Jun  4 18:54 ..
-rw-r--r-- 1 user   user      52 Jun 12 17:10 .. 
```

Right off the bat, we can see that in the directory `/home/user`, there is a file named `..`. That will be hard to `cat`, or do much else to, as the shell will assume we are referencing the directory `..`.

Now it comes down to how we can tell bash that we mean that file. The first thing that came to mind is to reference the file by it's inode number, something that was top of mind after [PlaidCTF's "Filesystem Based Strcmp go Brr" challenge](https://github.com/lyellread/ctf-writeups/blob/master/2020-plaidctf/file-system-based-strcmp-go-brrrr/README.md). 

To go about finding the inode number, we can tack on the `i` flag to `ls`, as so:

```bash
user@host:/home/user$ ls -lahi
ls -lahi
total 12K
8257688 dr-xr-xr-x 1 nobody nogroup 4.0K Jun 12 17:10 .
8257687 drwxr-xr-x 1 user   user    4.0K Jun  4 18:54 ..
8257689 -rw-r--r-- 1 user   user      52 Jun 12 17:10 .. 
```

Knowing that, we can proceed to print it as follows:

```bash
user@host:/home/user$ find . -inum 8257689 -exec cat {} \;
find . -inum 8257689 -exec cat {} \;
flag{we_should_have_been_worried_about_u2k_not_y2k}
```

And that's all there is to it. 

~ Lyell