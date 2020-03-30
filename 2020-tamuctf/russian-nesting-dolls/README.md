# RUSSIAN_NESTING_DOLLS Writeup

### Prompt

Our monitoring systems noticed some funny-looking DNS traffic on one of our computers. We have the network logs from around the time of the incident. Want to take a look?

Files: [netlogs.pcap](netlogs.pcap)

### Solution

Opening the PCAP up in `wireshark` shows that there are quite a few (37991) `DNS` packets, as well as a smattring of others (`Statistics` > `Protocol Hierarchy`). Let's look at the remaining packets first, as there are only a few of them:

- There's 1 `mDNS` packet, which appears to have no consequence.
- There are 8 `DHCP` packets that also appear inconsequential
- There are quite a few `FTP` packets, from which we can glean a username and password `goodag` and `howdy` respectively.
- There are 3 `FTP-DATA` packets, which include a PGP Public and Private keys, as well as a directory listing (see below).

[PGP Public Key](public-key)
[PGP Private Key](private-key)
Directory Listing:
```
drwxr-xr-x    2 1000     1000         4096 Nov 26 21:37 Desktop
drwxr-xr-x    2 1000     1000         4096 Nov 26 21:37 Documents
drwxr-xr-x    2 1000     1000         4096 Nov 26 21:37 Downloads
drwxr-xr-x    2 1000     1000         4096 Nov 26 21:37 Music
drwxr-xr-x    2 1000     1000         4096 Nov 26 21:37 Pictures
drwxr-xr-x    2 1000     1000         4096 Nov 26 21:37 Public
drwxr-xr-x    2 1000     1000         4096 Nov 26 21:37 Templates
drwxr-xr-x    2 1000     1000         4096 Nov 26 21:37 Videos
-rw-r--r--    1 1000     1000         8980 Nov 24 21:15 examples.desktop
-rw-------    1 1000     1000         3589 Nov 27 03:20 priv
-rw-------    1 1000     1000         1698 Nov 27 03:20 pub
```

This directory listing does not look to have much interesting to it, but the PGP keys do. 

Now we turned our attention to the 37991 `DNS` packets. These each contain a query to a site in the format `x6U3gvbExVWkk4U1gzWVU2L2FnRVNYMW5ZTHRjZ0d5b1NiNENYNlFOTVE-tamu1e100net`, where the prefix (`x6U3gvbExVWkk4U1gzWVU2L2FnRVNYMW5ZTHRjZ0d5b1NiNENYNlFOTVE`) looks to be base64 data, and these packets are all in a sequence. 

Let's look at the first packet: it contains base64 data `LS0tLS1CRUdJTiBQR1AgTUVTU0FHRS0tLS0tClZlcnNpb246IEdudVBHI` that decodes to 
```
-----BEGIN PGP MESSAGE-----
Version: GnuPG
```

[This script](get_pgp_from_dns_b64.py) extracts all that data (and ignores repeated packets and `mDNS` packet) and contactenates it into [message.pgp](message.pgp). 

Then, we need to remove the second layer of nested doll, and extract the message:
```bash
$ gpg --import public-key 
gpg: key 18ABAFED3849EB2E: "Ol' Rock <olrock@aggie.network>" not changed
gpg: Total number processed: 1
gpg:              unchanged: 1

$ gpg --import private-key 
gpg: key 18ABAFED3849EB2E: "Ol' Rock <olrock@aggie.network>" not changed
gpg: key 18ABAFED3849EB2E: secret key imported
gpg: Total number processed: 1
gpg:              unchanged: 1
gpg:       secret keys read: 1
gpg:  secret keys unchanged: 1

$ gpg --output out --decrypt message.pgp
gpg: encrypted with 2048-bit RSA key, ID C5372B2EB5E56F58, created 2019-11-27
      "Ol' Rock <olrock@aggie.network>"

```

To decrypt, the password `howdy` is used when prompted. We get [out](out), which `file` tells us is a `gzip` archive.

```bash
cp out out.gz
gunzip -c out.gz > ./out-2
```

This creates [out-2](out-2), which again is passed to `file` which tells us it is a `tar` archive.

```bash
cp out-2 out-2.tar
tar -xvf out-2.tar 
```

This extraction creates a bunch of weird files:
```
./..........encoded
./...encoded
./....encoded
./.....encoded
./.......encoded
./......encoded
./...........encoded
./........encoded
./............encoded
./.........encoded
```

Funky! Let's see what these are. They are each about 156K large (they seem to have 157696 characers each), and all contain data that looks like more base64 data. To make sense of these, we put them into [CyberChef](https://gchq.github.io/CyberChef/), and looked for any indication of what these were. Of all of them, we identified that [........encoded](........encoded) starts with [jpeg magic bytes](https://www.ntfs.com/jpeg-signature-format.htm). [Cyber Chef Link](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)To_Hexdump(16,false,false)&input=YWFhYS85ai80QUFRU2taSlJnQUJBZ0FBWkFCa0FBRC83QUFSUkhWamEza0FBUUFFQUFBQVBBQUEvKzRBSmtGa2IySmxBR1RBQUFBQUFRTUEKRlFRREJnb05BQUE3TUFBQVJJb0FBSHY0QUFEbG52L2JBSVFBQmdRRUJBVUVCZ1VGQmdrR0JRWUpDd2dHQmdnTERBb0tDd29LREJBTQpEQXdNREF3UURBNFBFQThPREJNVEZCUVRFeHdiR3hzY0h4OGZIeDhmSHg4Zkh3RUhCd2NOREEwWUVCQVlHaFVSRlJvZkh4OGZIeDhmCkh4OGZIeDhmSHg4Zkh4OGZIeDhmSHg4Zkh4OGZIeDhmSHg4Zkh4OGZIeDhmSHg4Zkh4OGZIeDhmLzhJQUVRZ0Nsd09OQXdFUkFBSVIKQVFNUkFmL0VBTlVBQVFFQkFRRUJBUUVBQUFBQUFBQUFBQUFCQXdJRUJRWUhBUUVCQVFFQkFRRUFBQUFBQUFBQUFBQUFBUUlEQkFVRwpFQUFCQXdJRkJBTUJBQU1BQXdFQkFBQUJBQkVDRUFNZ01FQWhFbEJnTVFSQkloTXlJeFFGY0RNa1FoVVJBQUVDQXdVRkJnVUNCUVFECkFBQUFBQUVBRVNFeEFoQWdRVkVTUUdGeElnTXdVR0NCa1RLeHdVSlNFNkhSY09GaWdpT0Fjak5Ua3VJa0VnRUFBQUFBQUFBQUFBQUEKQUFBQUFBRFFFd0VBQWdFREF3UUJBd1VCQVFBQUFBQUJBQkVoRURGQklGRmhNRUJ4Z1pHaHNjRlFZUERSNGZGdy85b0FEQU1CQUFJUgpBeEVBQUFINFA2TDg2cEVxd0ZJQVVCUWdGQUFRdFFBQ2doU0FvUUZBUXFBaWdVZ0tnc0VMSTgvRDBaZWYwZFIzR2g2ODNVOG01ejI0CmRlcnpCU0FBc0JSQlFMQUFVZ0FLaUFBQUFxS0lBQUFvZ0lvRlFJVWdBVUNnUUNnQUpRQUNoQlJBVkJGRklFdGdBS1FFQ2lvQkpRRVkKOGUySG05SFMyTjQwVGZPclo1TjU3OXZqdThGRUFLQUVCUUFCQ2dBRUFvQUFBQXNBQUlVRWdvZ3BDa1VVQUNBVUFBQUFxQ2dBQkFDawpvSW9JVUNvSUJGQXFTZ0VvQkpjODc4WGo5blV2Y21zZExzbm96ZlB1YzkrRjlQblVBQVFBb0pTQlFFS0lsVkFBQUJRUUFGQ0toU0JLCkxBUUhTSVVFQlZoU0FvQUVMVUFGSVVBQUZTQUZFQ2tBQUFBQUFBQUlKWkhpOGZ1bWRkeDBuUnBHMGVxWHc5Y1BiNUdvQUJVQUFBQUE). We convert this to a jpeg using an [online tool](https://onlinejpgtools.com/convert-base64-to-jpg), and get [8dot_out.jpg](8dot_out.jpg):

![Image](8dot_out.jpg)

That may look like a shark, but it's actually a nesting doll (what do you know!). I use [stegsolve](https://github.com/zardus/ctf-tools/tree/master/stegsolve) to examine the image. In stegsolve, under `Analyze` > `File Format` (which you know has something interesting when stegsolve hangs for a second when opening), we can see that, indeed, there's quite a bit here:

```
End of Image 
Additional bytes at end of file = 57524 
Dump of additional bytes: Hex: 
89504e470d0a1a0a
```

`89` `50` `4e` ... That looks like PNG [Magiv Bytes](https://asecuritysite.com/forensics/magic) :). We need to chop the PNG off the end of this JPG, we do that using [extract_png.py](extract_png.py), and we get [out.png](out.png).

![Image](out.png)

```
gigem{dont_you_just_love_a_good_pcap?}
```

~CaptainGeech, Lyell Read
