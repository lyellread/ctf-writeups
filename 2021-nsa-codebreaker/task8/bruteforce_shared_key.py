import multiprocessing
import os
import time
import datetime
import hashlib
import nacl.secret
import nacl.utils
import sys

"""
Usage:
    bruteforce_shared_key.py <wordlist> <offset>
"""

# Packet Bytes to Check

packet_bytes = [
    (
        1615897619,  # turned out to be ..22
        bytes.fromhex(
            "e2391e11eeef7575d0b4a860545ea93a0fb3c610fceee2f30fab78003304e673a12fa1a5f4c5d8c27d2d0628f7dd93ca69b6b9d03b561e4e6cf95ae95e3ba4d18d5abf6f6c98d9c8e93cb013e0ea"
        ),
    ),
    (
        1615897640,  # turned out to be ..42
        bytes.fromhex(
            "ea9415b6f3b3ba2a80517c335124aa3038b37ade75bc6e55bd594784d54f9497274c8f06e360b2277d75d35d83d73c5b7e9d38fd695533df6e4033623a007836e3822a00c6888196458cbee63d2f"
        ),
    ),
    (
        1615897726,  # turned out to be ..23
        bytes.fromhex(
            "4a7ab5d016808e96c7c98bb080549dc43db7e66c678d85b4b3b5ae1bb9941bae289b9fb4422ae32c51a8857d660bde3843ea29ea23ea490913e1b52fce13bd73576029cba9937bf465815e2e1ca0"
        ),
    ),
    (
        1615897722,  # turned out to be ..20
        bytes.fromhex(
            "404bbfffd01740266af9f67b494ef47b6a7ea4a2ca8c6193d625314df8561e94a478275d9b4fcdfe5be2469421d2dd925acd671792d2cd2f7b82648d193cb558e5ba8ab667c526ad6e12bd45bbca"
        ),
    ),
    (
        1615897682,  # turned out to be 83
        bytes.fromhex(
            "13fcec4ee868c0cb3aa0ca94f5df3ea2e9420db68fac9721a0e6a39d108401a93adb29e4c7d68042ab3928c29335870ba3bb42692e8dea9ca90a99961ffe9c42081ce7b4594269703af0aa077a13"
        ),
    ),
    (
        1615897651,  # turned out to be ..52
        bytes.fromhex(
            "3750c8fa6f9ea3a9b54ce99ae4080748bb319e4bef2540ca51b7724d5040b26ad2e96b2ecf9133daf0fd2c75b2271eafd1d73a4e7ee0d750c8117d501cc2ffeb70675835477fa23f3b1128ac8256",
        ),
    ),
]


def test(arg):
    usernames = arg[0]
    num = arg[1]
    perc = arg[2]
    offset = arg[3]

    for username in usernames:
        username = username.lower()
        print(f"[{perc}%] Brute Forcing Username #{num}: {username}")

        # Check all Versions
        for v1 in range(10):
            for v2 in range(10):
                for v3 in range(10):
                    for v4 in range(10):

                        # Generate Version String
                        version_str = f"{v1}.{v2}.{v3}.{v4}"

                        # Check each capture from above
                        for cap in packet_bytes:

                            # Check any possible timestamp given offset argument
                            for timestamp in range(
                                cap[0] - offset, cap[0] + offset + 1
                            ):

                                # Prepare secret box to be used in decryption
                                box = nacl.secret.SecretBox(
                                    bytes.fromhex(
                                        hashlib.sha256(
                                            (
                                                f"{username}+{version_str}+{timestamp}"
                                            ).encode()
                                        ).hexdigest()
                                    )
                                )

                                # Try to decrypt. If we succeed, print and write result
                                try:
                                    plaintext = box.decrypt(ciphertext=cap[1][4:])
                                    print(f"FOUND A UUID STRING: {plaintext.hex()}")
                                    print(
                                        f"--> username: {username}, version: {version_str}, timestamp: {timestamp}, cap: {cap[1].hex()}."
                                    )

                                    with open("out.txt", "a") as f:
                                        f.write(plaintext.hex())
                                        f.write("\n")
                                        f.write(
                                            f"--> username: {username}, version: {version_str}, timestamp: {timestamp}, cap: {cap[1].hex()}.\n"
                                        )

                                # Error being raised indicates the decryption was not successful. Continue
                                except nacl.exceptions.CryptoError as e:
                                    pass

                                # Print any non-CryptoError Exceptions
                                except Exception as e:
                                    print(e)
    return False


def worker_main(queue):
    while True:
        item = queue.get(True)
        test(item)


if __name__ == "__main__":

    the_queue = multiprocessing.Queue()

    the_pool = multiprocessing.Pool(
        multiprocessing.cpu_count(), worker_main, (the_queue,)
    )

    assert (
        len(sys.argv) == 3
    ), "Not enough arguments. Usage: bruteforce_shared_key.py <wordlist> <offset>"

    usernames = []
    with open(sys.argv[1]) as f:
        [usernames.append(x) for x in f.read().splitlines()]

    for i in range(len(usernames)):
        the_queue.put(
            (
                [usernames[i]],
                i,
                (int((10000 * i) / len(usernames)) / 100),
                int(sys.argv[2]),
            )
        )

    while True:
        time.sleep(100)
