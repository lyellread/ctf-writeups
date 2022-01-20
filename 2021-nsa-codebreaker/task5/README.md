# NSACC Task 5 Writeup

## Prompt

> A forensic analysis of the server you identified reveals suspicious logons shortly after the malicious emails were sent. Looks like the actor moved deeper into OOPS' network. Yikes.

> The server in question maintains OOPS' Docker image registry, which is populated with images created by OOPS clients. The images are all still there (phew!), but one of them has a recent modification date: an image created by the Prevention of Adversarial Network Intrusions Conglomerate (PANIC).

> Due to the nature of PANIC's work, they have a close partnership with the FBI. They've also long been a target of both government and corporate espionage, and they invest heavily in security measures to prevent access to their proprietary information and source code.

> The FBI, having previously worked with PANIC, have taken the lead in contacting them. The FBI notified PANIC of the potential compromise and reminded them to make a report to DC3. During conversations with PANIC, the FBI learned that the image in question is part of their nightly build and test pipeline. PANIC reported that nightly build and regression tests had been taking longer than usual, but they assumed it was due to resourcing constraints on OOPS' end. PANIC consented to OOPS providing FBI with a copy of the Docker image in question.

> Analyze the provided Docker image and identify the actor's techniques.

Downloads:

PANIC Nightly Build + Test Docker Image [image.tar](image.tar)

Category: Docker Analysis

Points: 300

## Solve

First we `load` and `inspect` the image using Docker.

```sh
docker image load -i image.tar
    Loaded image: panic-nightly-test:latest
docker image inspect panic-nightly-test
    ...
    "Cmd": [
        "./build_test.sh"
    ]
    ...
    "maintainer": "allman.joyce@panic.invalid",
    ...
```

The next step is to find the malicious binary. We will start up the image, and poke around:

```sh
docker run -it panic-nightly-test /bin/bash
```

This grants us a shell, and we can see the contents of the `build_test.sh` script:

```sh
#!/bin/bash

git clone https://git-svr-78.prod.panic.invalid/hydraSquirrel/hydraSquirrel.git repo

cd /usr/local/src/repo

./autogen.sh

make -j 4 install

make check
```

This script attempts to pull a repo down, and run a script within it. However, the url `git-svr-78.prod.panic.invalid/hydraSquirrel/hydraSquirrel.git` is not active. 

After some searching, we find that the binary `make` behaves strangely:

```
bash-5.1# make
ninja: *** No targets specified and no makefile found.  Stop.
bash-5.1# 
```

Therefore, our suspicious binary is `/usr/bin/make`. 
