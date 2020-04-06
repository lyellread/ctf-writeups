from pwn import *
from base64 import b64decode


while True:
    p = remote("snakeplusplus-01.play.midnightsunctf.se", 55555)

    p.sendline("2")
    p.sendline("")
    p.sendline("")

    with open("snake.ai", 'rb') as f:
        code = f.read()
    p.sendline(code)

    try:
        p.recvuntil("Result: ")
    except:
        p.interactive()

    x = p.recvline()
    if b"midnight" in x:
        print(x)
        exit(0)
    try:
        y = b64decode(x)
        print(y)
        if b"midnight" in y:
            print(y)
            exit(0)
    except:
        print(x)
    p.close()
