# NSACC Task 2 Writeup

## Prompt

> NSA notified FBI, which notified the potentially-compromised DIB Companies. The companies reported the compromise to the Defense Cyber Crime Center (DC3). One of them, Online Operations and Production Services (OOPS) requested FBI assistance. At the request of the FBI, we've agreed to partner with them in order to continue the investigation and understand the compromise.

> OOPS is a cloud containerization provider that acts as a one-stop shop for hosting and launching all sorts of containers -- rkt, Docker, Hyper-V, and more. They have provided us with logs from their network proxy and domain controller that coincide with the time that their traffic to the cyber actor's listening post was captured.

> Identify the logon ID of the user session that communicated with the malicious LP (i.e.: on the machine that sent the beacon *and* active at the time the beacon was sent).

Downloads:

Subnet associated with OOPS [oops_subnet.txt](oops_subnet.txt)
Network proxy logs from Bluecoat server [proxy.log](proxy.log)
Login data from domain controller [logins.json](logins.json)

Category: Log Analysis

Points: 50

## Solve

Find in the [proxy.log](proxy.log) an entry that communicated with LP (from task 1: `10.61.181.46`). We can tell that this is what we are looking for as it has an IP address within the OOPS subnet provided in [oops_subnet.txt](oops_subnet.txt).


```
2021-03-16 08:27:56 43 198.18.252.163 200 TCP_MISS 12734 479 GET http thrqt.invalid pressure - - DIRECT 10.61.181.46 application/octet-stream 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN)' PROXIED none - 198.18.255.81 SG-HTTP-Service - none -
```

That log entry took place at `2021-03-16 08:27:56`. The header for the [proxy.log](proxy.log) file contains the following information about the software and crucially about the timezone: 

```
#Software: SGOS 6.7.5.3
#Version: 1.0
#Date: 2021-04-16 13:51:09 EST (UTC-0400)
```

This indicates that we are offset from UTC by `-04:00` hours. When we examine the entries in the [logins.json](logins.json) file, we can see it is offset from UTC by `+00:00`: 

```
... "TimeCreated": "2021-03-16T10:18:52.4071661+00:00" ...
```

Using this new time, and by parsing the [logins.json](logins.json) file into a CSV, we can filter by target IP (`198.18.252.163`) and time, we can see that there is exactly one session to the target machine which is open at that time, the others have seen logoff events before our time range. From this entry in [logins.json](logins.json), we can extract the Logon ID.