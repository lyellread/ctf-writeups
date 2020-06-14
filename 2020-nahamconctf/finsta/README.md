# Finsta

50 points

### Prompt

> This time we have a username. Can you track down `NahamConTron`?

### Solution

I used the `namechk` tools from the [OSINT Framework Site](https://osintframework.com/). Specifically, I used `OSINT Framework` > `Username` > `Username Search Engines` > [`Namechk`](https://namechk.com/), similarly to in AUCTF. 

`namechk` tells me that there are claimed usernames for the name `NahamConTron` for many sites, including Instagram. 

[!Image](claimed.png)

Checking out [the Instagram account](https://www.instagram.com/NahamConTron/), we get the flag.

```
flag{i_feel_like_that_was_too_easy}
```

~ Lyell