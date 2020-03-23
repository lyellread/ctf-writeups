from scapy.all import *
import base64

import string

packets = rdpcap("netlogs.pcap")
print "parsed {} packets".format(len(packets))

b64_data = ""

counter = 0

for p in packets:
    if p.haslayer(DNSQR):
        name = p[DNSQR].qname
        if "-tamu" not in name:
            counter += 1
            continue
        val = name.split("-tamu")[0]

        if val not in b64_data:
            b64_data += val

        # find bad data
        # try:
        #     for b in base64.b64decode(b64_data + "===")[-30:]: # ensure padding
        #         if b not in string.printable:
        #             print "counter: {}".format(counter)
        #             print name
        #             raise Exception
        # except TypeError:
        #     # print "skipped {}".format(counter)
        #     pass

    counter += 1

print "got b64 payload, len={}".format(len(b64_data))

filepath = "dns_dump.pgp"
with open(filepath, "w") as f:
    f.write(base64.b64decode(b64_data + "==="))
