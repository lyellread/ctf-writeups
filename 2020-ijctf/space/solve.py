
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from random import randrange
import string

alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
iv = md5(b"ignis").digest()

flag = "ijctf{i am not the real flag :)}"
message = b"Its dangerous to solve alone, take this" + b"\x00"*9
messageenc = b64decode("NeNpX4+pu2elWP+R2VK78Dp0gbCZPeROsfsuWY1Knm85/4BPwpBNmClPjc3xA284")

def flag(a,i,i2,j,j2):
    flagenc = b64decode("N2YxBndWO0qd8EwVeZYDVNYTaCzcI7jq7Zc3wRzrlyUdBEzbAx997zAOZi/bLinVj3bKfOniRzmjPgLsygzVzA==")
    #flagenc = b64decode("NeNpX4+pu2elWP+R2VK78Dp0gbCZPeROsfsuWY1Knm85/4BPwpBNmClPjc3xA284")
    key1 = a[0].encode() + a[1].encode() + b'\x00'*14
    key2 = a[2].encode() + a[3].encode() + b'\x00'*14
    key3 = i.encode() + i2.encode() + b'\x00'*14
    key4 = j.encode() + j2.encode() + b'\x00'*14

    keys = []
    keys.append(key4)
    keys.append(key3)
    keys.append(key2)
    keys.append(key1)
    for key in keys:
        cipher = AES.new(key, AES.MODE_CBC, IV=iv)
        flagenc = cipher.decrypt(flagenc)
    print(flagenc)
    exit()

encs = []
d = {}
for i in alphabet:
    for i2 in alphabet:
        for j in alphabet:
            for j2 in alphabet:
                key = i.encode() + i2.encode() + b'\x00'*14
                cipher = AES.new(key, AES.MODE_CBC, IV=iv)
                newmessage = cipher.encrypt(message)

                key = j.encode() + j2.encode() + b'\x00'*14
                cipher = AES.new(key, AES.MODE_CBC, IV=iv)
                newmessage = cipher.encrypt(newmessage)
                d[newmessage] = (i,i2,j,j2)
    print(i)

print("done phase 1")

for i in alphabet:
    for i2 in alphabet:
        for j in alphabet:
            for j2 in alphabet:
                key = j.encode() + j2.encode() + b'\x00'*14
                cipher = AES.new(key, AES.MODE_CBC, IV=iv)
                newmessage = cipher.decrypt(messageenc)

                key = i.encode() + i2.encode() + b'\x00'*14
                cipher = AES.new(key, AES.MODE_CBC, IV=iv)
                newmessage = cipher.decrypt(newmessage)
                if newmessage in d:
                    print("matched")
                    print(d[newmessage])
                    print(i)
                    print(i2)
                    print(j)
                    print(j2)
                    flag(d[newmessage],i,i2,j,j2)
    print(i)
