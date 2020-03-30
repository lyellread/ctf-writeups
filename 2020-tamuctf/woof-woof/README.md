# WOOF_WOOF Writeup

### Prompt

(I did not get the prompt text in time, and admin closed access to the challs when the CTF ended :()

The instructions mentioned charset A-Z and '-' and '@', with flag format `GIGEM-...`.

[reveille.png](reveille.png)

### Solution

After running strings on the image to no result, we open this image up in [stegsolve](https://github.com/zardus/ctf-tools/tree/master/stegsolve), and examine the file format `Analyze` > `File Format`. We see the usual stuff, except for:

```
Comment data Length: 1aa (426) Dump of data: Hex: 01aa776f6f662077 6f6f66206261726b 2072756666206261 726b206261726b20 7275666620776f6f 6620776f6f662062 61726b2072756666 206261726b207275 666620776f6f6620 776f6f6620727566 6620776f6f662062 61726b206261726b 206261726b206261 726b20776f6f6620 7275666620776f6f 66206261726b2062 61726b2072756666 20776f6f6620776f 6f6620776f6f6620 776f6f6620776f6f 6620727566662077 6f6f6620776f6f66 206261726b207275 666620776f6f6620 7275666620626172 6b20776f6f662077 6f6f66206261726b 20776f6f66206261 726b207275666620 6261726b20626172 6b206261726b2072 75666620776f6f66 2072756666206261 726b20776f6f6620 776f6f6620776f6f 6620776f6f662072 75666620776f6f66 206261726b20776f 6f66206261726b20 7275666620626172 6b20776f6f662077 6f6f6620776f6f66 207275666620776f 6f6620776f6f6620 776f6f6620776f6f 6620776f6f662072 75666620776f6f66 206261726b206261 726b206261726b20 7275666620776f6f 66206261726b2062 61726b206261726b 206261726b20776f 6f66 Ascii: ..woof w oof bark ruff ba rk bark ruff woo f woof b ark ruff bark ru ff woof woof ruf f woof b ark bark bark ba rk woof ruff woo f bark b ark ruff woof wo of woof woof woo f ruff w oof woof bark ru ff woof ruff bar k woof w oof bark woof ba rk ruff bark bar k bark r uff woof ruff ba rk woof woof woo f woof r uff woof bark wo of bark ruff bar k woof w oof woof ruff wo of woof woof woo f woof r uff woof bark ba rk bark ruff woo f bark b ark bark bark wo of
```

Interesting. Let's clean that up in a text editor...

```
woof woof bark ruff bark bark ruff woof woof bark ruff bark ruff woof woof ruff woof bark bark bark bark woof ruff woof bark bark ruff woof woof woof woof woof ruff woof woof bark ruff woof ruff bark woof woof bark woof bark ruff bark bark bark ruff woof ruff bark woof woof woof woof ruff woof bark woof bark ruff bark woof woof woof ruff woof woof woof woof woof ruff woof bark bark bark ruff woof bark bark bark bark woof 
```

I've been waiting for a challenge in morse for a long time, so I immediately tested it for morse code. To be a candidate, it must have 3 different 'things' and one of those as a delineator, which can only occur once at a time. 

The first character of our flags is `G`, and morse `G` is `--.`. Great! We now know that `woof` = `-`, `bark` = `.`, `ruff` = delineator. Let's convert that out:

```
--. .. --. . -- -....- -.. ----- --. - .--.-. ... - .---- -.-. .--- ----- -... -....-
```

Next, we use an [online tool](http://www.unit-conversion.info/texttools/morse-code/) to convert that morse to the following text:

```
gigem?d0gt?st1cj0b?
```

We know that the first `?` must be a `-` because of the flag fomat given, and the last `?` is the same morse character, so that one is too. The middle `?` is a different morse code, though, so it must be the last letter of our charset, `@`.

```
GIGEM-D0GT@ST1CJ0B-
```

~Lyell Read
