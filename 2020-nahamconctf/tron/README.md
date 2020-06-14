# Tron

75 points

### Prompt

> `NahamConTron` is up to more shenanigans. Find his server.

### Solution

I used the `namechk` tools from the [OSINT Framework Site](https://osintframework.com/). Specifically, I used `OSINT Framework` > `Username` > `Username Search Engines` > [`Namechk`](https://namechk.com/), similarly to in AUCTF. 

`namechk` tells me that there are claimed usernames for the name `NahamConTron` for many sites:

![Image](claimed.png)

Now that we have exhausted Instagram, I opened up all the other sites with claimed usernames for `NahamConTron` and systematically eliminated them. I ended up at the GitHub account owned by `NahamConTron`, and it included [a dotfiles repo](dotfiles). This in turn contains [a bash history file](dotfiles/.bash_history) that gives us the command that was run to access the server: 

```bash
ssh -i config/id_rsa nahamcontron@jh2i.com -p 50033
```

Now we just need the key, which conveniently and innapropriately is in the config repo. Running that command first gives us this error: 

```bash
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0664 for 'config/id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "config/id_rsa": bad permissions
nahamcontron@jh2i.com's password: 
```

This is fixed with a quick `chmod 600 config/id_rsa` and then:

```bash
ssh -i config/id_rsa nahamcontron@jh2i.com -p 50033
nahamcontron@94f05a972db8:~$ cat flag.txt
flag{nahamcontron_is_on_the_grid}
```

~ Lyell