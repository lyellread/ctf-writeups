import hashlib
import nacl.secret
import nacl.utils
from packet_bytes import PacketBytes

stream0_key = "anisa+1.5.9.1+1615897622"
stream1_key = "ngan+0.0.1.0+1615897642"
stream2_key = "root+3.3.4.3+1615897652"
stream4_key = "xiaofeng+0.9.2.2+1615897683"
stream5_key = "vcsrv+1.4.9.0+1615897720"
stream6_key = "rozanna+1.7.6.6+1615897723"

from streams.stream0 import stream0
from streams.stream1 import stream1
from streams.stream2 import stream2
from streams.stream4 import stream4
from streams.stream5 import stream5
from streams.stream6 import stream6

pb = PacketBytes()

with open("decoded.txt", "w") as f:
    f.write("Decoded for Stream 0\n-----------------------------------\n")
    box = nacl.secret.SecretBox(
        bytes.fromhex(hashlib.sha256((stream0_key).encode()).hexdigest())
    )
    for s in stream0:
        try:
            p = box.decrypt(ciphertext=s[4:])
            f.write(p.hex() + "\n")
            f.write(pb.parse(p) + "\n\n")
        except Exception as e:
            f.write(str(e) + "\n")

    f.write("\n\n\nDecoded for Stream 1\n-----------------------------------\n")
    box = nacl.secret.SecretBox(
        bytes.fromhex(hashlib.sha256((stream1_key).encode()).hexdigest())
    )
    for s in stream1:
        try:
            p = box.decrypt(ciphertext=s[4:])
            f.write(p.hex() + "\n")
            f.write(pb.parse(p) + "\n\n")
        except Exception as e:
            f.write(str(e) + "\n")

    f.write("\n\n\nDecoded for Stream 2\n-----------------------------------\n")
    box = nacl.secret.SecretBox(
        bytes.fromhex(hashlib.sha256((stream2_key).encode()).hexdigest())
    )
    for s in stream2:
        try:
            p = box.decrypt(ciphertext=s[4:])
            f.write(p.hex() + "\n")
            f.write(pb.parse(p) + "\n\n")
        except Exception as e:
            f.write(str(e) + "\n")

    f.write("\n\n\nDecoded for Stream 4\n-----------------------------------\n")
    box = nacl.secret.SecretBox(
        bytes.fromhex(hashlib.sha256((stream4_key).encode()).hexdigest())
    )
    for s in stream4:
        try:
            p = box.decrypt(ciphertext=s[4:])
            f.write(p.hex() + "\n")
            f.write(pb.parse(p) + "\n\n")
        except Exception as e:
            f.write(str(e) + "\n")

    f.write("\n\n\nDecoded for Stream 5\n-----------------------------------\n")
    box = nacl.secret.SecretBox(
        bytes.fromhex(hashlib.sha256((stream5_key).encode()).hexdigest())
    )
    for s in stream5:
        try:
            p = box.decrypt(ciphertext=s[4:])
            f.write(p.hex() + "\n")
            f.write(pb.parse(p) + "\n\n")
        except Exception as e:
            f.write(str(e) + "\n")

    f.write("\n\n\nDecoded for Stream 6\n-----------------------------------\n")
    box = nacl.secret.SecretBox(
        bytes.fromhex(hashlib.sha256((stream6_key).encode()).hexdigest())
    )
    for s in stream6:
        try:
            p = box.decrypt(ciphertext=s[4:])
            f.write(p.hex() + "\n")
            f.write(pb.parse(p) + "\n\n")
        except Exception as e:
            f.write(str(e) + "\n")
