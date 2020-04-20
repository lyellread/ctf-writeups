# Dangit Retrospective Writeup - 100pts

## Prompt

> While many fine clients exist, only two deserve to be called [porcelains](http://dangit.pwni.ng/)

## Solution

On first examination, the site provided appears to allow the user to download the latest log from a link. This log is located at http://dangit.pwni.ng/log. Combined with the fact that this challenge is called dan***git*** and that this is the "latest" log, we check that the root directory of the site contains a `.git` folder: 

```bash
$ wget http://dangit.pwni.ng/.git/config
$ cat config
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
[user]
    email = nonexistent@f0xtr0t.com
    name = Nobody
```

Looks like we got something. Next, we used [GitTools](https://github.com/internetwache/GitTools/) to pull down the repo. 

```bash
bash gitdumper.sh http://dangit.pwni.ng/.git/ ../git-repo-dump
```

It finds a bunch of objects, logs, and whatnot. This is located in [git-repo-dump.zip](git-repo-dump.zip) We use GitTools Extractor on it:

```bash
bash extractor.sh ../../git-repo-dump ../../git-repo-dump-extracted
```

Let's examine that further... `git log -p > ../git-log.txt` ([logs](git-log.txt)). Nothing important there, except a couple intriguing commits. It looks like each time, they replace the contents of `log` with somethings else... 

We checked our work over a couple hours of manual work, but nothing at all showed up... Back to the prompt, then! 

The prompt makes references to porcelains. Porcelains are the user-facing commands that git has, as opposed to the plumbing commands - those that are intended to be used by scripts and the like. We searched the entire clue, and came up with [Magit](https://magit.vc/) comes up, and it appears to be an emacs `git` client, so it fits the clue. After reading the docs, we determined that this was not the way to go.

This is where we left the problem during the challenge. After the fact, based on [a writeup by null2root](https://ctftime.org/writeup/20046), we were in fact on the right path. oof. 

Basically, we just needed to read the docs. They were using Magit with [wip modes](https://magit.vc/manual/magit/Wip-Modes.html) - these store some tracked items to a `wip` ref in refs as a backup in case changes are delteted that were not meant to be. Cool feature. 

Therefore, we need to pull those refs down too when we pull the repository. To do that, I have to get GitDumper to collect those additional refs (these changes are implemented in [GitTools-Magit](GitTools-Magit). 

```
+    QUEUE+=('/refs/wip/index/refs/heads/master')
+    QUEUE+=('/refs/wip/wtree/refs/heads/master')
```

Then, we re-run both the GitTools Dumper and Extractor, and look through all extracted commits' files. 

```
