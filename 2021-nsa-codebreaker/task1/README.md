# NSACC Task 1 Writeup

## Prompt

The NSA Cybersecurity Collaboration Center has a mission to prevent and eradicate threats to the US Defense Industrial Base (DIB). Based on information sharing agreements with several DIB companies, we need to determine if any of those companies are communicating with the actor's infrastructure.

You have been provided a capture of data en route to the listening post as well as a list of DIB company IP ranges. Identify any IPs associated with the DIB that have communicated with the LP.

Downloads:

Network traffic heading to the LP [capture.pcap](capture.pcap)
DIB IP address ranges [ip_ranges.txt](ip_ranges.txt)

Categories: Network Forensics, Command Line

Points: 25

## Solve

Start by getting all the active IPs in [capture.pcap](capture.pcap).

```sh
$ tshark -r capture.pcap -q -z ip_hosts,tree

=================================================================================================================================
IPv4 Statistics/All Addresses:
Topic / Item      Count         Average       Min val       Max val       Rate (ms)     Percent       Burst rate    Burst start
---------------------------------------------------------------------------------------------------------------------------------
All Addresses     196                                                     0.0009        100%          0.1100        0.000
 10.61.181.46     196                                                     0.0009        100.00%       0.1100        0.000
 10.114.130.133   40                                                      0.0002        20.41%        0.0700        20.508
 10.64.235.249    34                                                      0.0001        17.35%        0.1100        0.000
 172.26.157.145   28                                                      0.0001        14.29%        0.0700        106.349
 10.99.63.183     25                                                      0.0001        12.76%        0.0700        62.340
 192.168.99.33    18                                                      0.0001        9.18%         0.0700        30.950
 10.8.135.112     18                                                      0.0001        9.18%         0.0700        101.556
 198.18.251.111   11                                                      0.0000        5.61%         0.1100        57.275
 192.168.132.101  11                                                      0.0000        5.61%         0.1100        228.929
 10.4.15.171      11                                                      0.0000        5.61%         0.1100        201.246

---------------------------------------------------------------------------------------------------------------------------------
```

Next, we include these IP addresses in a script which will check each of the subnets for each of our IPs, to see which are in the DIB. This script ([insubnet.py](insubnet.py)) is as follows:

```python
import ipaddress

i = open("ip_ranges.txt", "r")
o = open("out.txt", "w")

lines = i.read().splitlines()

cap_ips = [
    "10.61.181.46",
    "10.114.130.133",
    "10.64.235.249",
    "172.26.157.145",
    "10.99.63.183",
    "192.168.99.33",
    "10.8.135.112",
    "198.18.251.111",
    "192.168.132.101",
    "10.4.15.171",
]

for subnet in lines:
    net = ipaddress.IPv4Network(subnet)
    for ip in cap_ips:
        if ipaddress.IPv4Address(ip) in net:
            o.write(f"{ip}\n")

i.close()
o.close()
```

When we run this, we see that it produces 4 IP addresses as output:

```
198.18.251.111
10.8.135.112
172.26.157.145
192.168.99.33
```

Those IPs are the IPs within the DIB which are compromised and talking with the LP. Further, we learn that the LP (the most common occurring IP address in [capture.pcap](capture.pcap)) is at IP `10.61.181.46`.