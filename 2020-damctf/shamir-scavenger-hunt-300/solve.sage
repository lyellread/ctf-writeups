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

    def reconstruct(self, shares, password_subset):
        password_points = self.find_password_points(password_subset)
        print(password_points)
        print(shares)
        poly = self.Rx.lagrange_polynomial(shares + password_points)
        flag = poly(0)
        return flag

if __name__ == '__main__':
    #from passwords import passwords
  
    passwords = ["shamir_memory_mgmt_is_optional",
    "shamir_stack_smashing_detected",
    "shamir_segmentation_fault",
    "shamir_is_this_in_standard_flag_format?",
    "shamir_babytcache101",
    "shamir_pineapple_not_pizza",
    "shamir_scsi_is_yummy",
    "shamir_siLANCE",
    "shamir_nvme_is_speedy_boi",
    "shamir_i_won't_STANd_by_this",
    "shamir_call_the_ambuLANCE",
    "shamir_lattices_are_magic",
    "shamir_wuddup_highyell",
    "shamir_why_are_there_flags",
    "shamir_thanos_did_nothing_wrong",
    "shamir_crypto_is_hard_pwn_is_life",
    "shamir_ppp_has_too_many_wins",
    "shamir_wants_sra_not_rsa_but_got_sss",
    "shamir_evasion_wen_eta"] 
   
    k = 18

    print(("Welcome to Shamir Secret Sharing. There are {} passwords and you will\n"
           "need {} of them, together with the shares below, to find the flag.\n").format(len(passwords), k))

    print("[*] Generating Shares\n")
    
    shamir = Shamir(k)

    shares = [(1, 0xc9e206211db59fe759a2fc6051553603378be33a713178a9422e3c1832221ab8),
                (2, 0xb8658d61b1f41b82994368acc3b53af4b8a7312421cbf02f6ecca35e8aabb807),
                (3, 0x78423b78426ca11099ff206e7ef926d9dbf0fd88158aea6900af66101e84be76),
                (4, 0xc5d95118f00baf1b283115c5e8ca33620fc781818c3dfc5c888530a281288477),
                (5, 0x6955fe1b4beb80c2cfcfb446409803524d2e9801004cca074e49d37394bac91c),
                (6, 0xa2792f70f50e56fefd87df4a0ccad36a9314213af560d22ed89854762d89bf6a),
                (7, 0x70c433b6c735cf2a6af3bb618aca2de2ec345b1c1e27978cf61757f171271c07),
                (8, 0xf14f707a3b0bfdea258415747fb366ad9329c0868832da3468b3b0fa292624f6),
                (9, 0xfa68cfa4f55488e4f8799ba5a9cfc3a03a80abefb697971ba6b728cd8bd1645f),
                (10, 0x2eda4b6e4b5c2aa184bc475622a17b1be852f9ca0ed793b9382c1c648c622a44),
                (11, 0x343bc66365671e8184d7f0537a37d6bfa12fd2b3e750fa441475bf1273cc536f),
                (12, 0xea873c18376c87a1def62f47000713ecbf8f809ed30513ab1b078170b0378078),
                (13, 0x95234c07bca419aa044c5d476b90aec20155ad81709cf92c675bf185c26e8997),
                (14, 0x10301526359450f94798fa7fde6a3a2e890cb4a3fedcdf0eb87b46ae0a84688c)]

    print("[+] Shares:")
    #list(map(lambda x: print("({}, {}),".format(x[0], hex(x[1]))), shares))
    #print()

    print("[*] Reconstructing:")
    flag = shamir.reconstruct(shares, random.sample(passwords, k))

    print(hex(int(flag)))