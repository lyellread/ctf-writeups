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
