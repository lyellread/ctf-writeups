# Leak Writeup

EkoParty CTF 2020 Git 1

## Prompt

Exact prompt has been forgotten. Linked to [this GitHub repo](ekolabs)

## Solution

This solution was quite obscure, as I approached this challenge in a `github` mindset, not a `ctf::misc` one. In light of this, I solved [the second challenge](../docs) first :P

When I got on to solving this one, it took me several runs through the full commit history of the repo before seeing this:

```bash
$ git log -p

...

commit c21dbf5185a4dbdb5b2bd2f3d1d3b266c3a2271e
Author: Matías A. Ré Medina <aereal@gmail.com>
Date:   Fri Sep 11 13:03:19 2020 -0400

    oops

...

diff --git a/.ssh/id_rsa.pub b/.ssh/id_rsa.pub
deleted file mode 100644
index 3cf8765..0000000
--- a/.ssh/id_rsa.pub
+++ /dev/null
@@ -1 +0,0 @@
-ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDRKS8bh5B2ctUxrS0JsrlYmw/pJPOr7N3BRtdrdswXu7An
oxohsNX7D6gPt5oHb3Map2XMSqj3ukDrBWgL/qfiCfU4g5Fc1J4QkedDTiDq2+YeanaLgKyPqrvrg+lZwOIhf
NXSliaxKI+YqgEy+n8s4ZhPGQYbpPjxDW/2ubn7iz60G+Px7q6BVvmRZlHe2IWylmG1WagL3pHFsJ83UyfgyF
dvPqYoDkjVK+/+E4IGXaKXwHst2sVC+6DEU1YF3jJXFqeunY+Q3/dgxWXIbF7qpYGGJusEziHzjPX7Kwk4t1a
W+afbREt7aDchx7KM/hDP/CBOYntwVA5qOG9L2rr6hbTTVMIqQxn2WAXtcBgc4Od4kMNAQt/8cvFsciApJ6RS
++FPIwx8gJJCe/OZYdRl19/Fv+j9xi7dIiET4SqCUPz3nionKvMjvPvrd/42P9xw+niY+3gJEtIZjMb66Let+
GuUew68bjz2DRlJSOtSNzP/MspNtUa5bY/4bmUMAHc= ekoparty-deploy@RUtPezc0NGFkN2ZlOGU2Y2U1Z
Tg4NWFkMjRlZWYyNDNiMWZkMTFkMGZiN2V9
```

That computer hostname does not look normal at all... Let's use [Cyber Chef](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)&input=UlV0UGV6YzBOR0ZrTjJabE9HVTJZMlUxWlRnNE5XRmtNalJsWldZeU5ETmlNV1prTVRGa01HWmlOMlY5Cg) to turn that into ASCII

```
EKO{744ad7fe8e6ce5e885ad24eef243b1fd11d0fb7e}
```

~ Lyell Read