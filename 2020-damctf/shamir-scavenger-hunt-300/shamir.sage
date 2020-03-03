from sage.all import *
import binascii
import hashlib
import random
import sys

def from_bytes(x):
    return int(binascii.hexlify(x), 16)

def from_string(x):
    return from_bytes(x.encode())

def into_string(i):
    return binascii.unhexlify(hex(i)[2:]).decode()

class Shamir:
    prime = 115285156253208754522866756368160904609172068524441322199995907783658333140303
    R = IntegerModRing(prime)
    Rx = R['x']

    def __init__(self, k):
        self.k = k

    def find_password_points(self, passwords):
        password_points = []
        for p in passwords:
            x = self.R(from_string(p))

            h = hashlib.sha512()
            h.update(p.encode())
            y = self.R(from_bytes(h.digest()))

            password_points.append((x, y))
        return password_points

    def share(self, secret, passwords):
        assert secret < self.prime

        password_points = self.find_password_points(passwords)
        poly = self.Rx.lagrange_polynomial([(0, secret)] + password_points)
        shares = []
        m = len(passwords) - self.k + 1
        for i in range(1, m + 1):
            shares.append((i, poly(i)))
        return shares

    def reconstruct(self, shares, password_subset):
        # Hint: use Rx.langrange_polynomial
        pass # REDACTED


if __name__ == '__main__':
    from passwords import passwords
    k = 18

    print(("Welcome to Shamir Secret Sharing. There are {} passwords and you will\n"
           "need {} of them, together with the shares below, to find the flag.\n").format(len(passwords), k))

    if len(sys.argv) < 2:
        print("Please provide secret to share")
    to_share = sys.argv[1]
    print("[*] Generating Shares\n")
    shamir = Shamir(k)
    shares = shamir.share(from_string(to_share), passwords)

    print("[+] Shares:")
    list(map(lambda x: print("({}, {}),".format(x[0], hex(x[1]))), shares))
    print()

    print("[*] Reconstructing:")
    flag = into_string(shamir.reconstruct(shares, random.sample(passwords, k)))
    print(flag)
