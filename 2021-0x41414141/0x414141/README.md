# 0x414141

## Prompt

I think offshift promised to opensource some of their code

author: notforsale

## Solution

First off, we navigate to the [offshift-dev](https://github.com/offshift-dev/assets/commits/master) github account, linked from the offshift site. Unfortunately, nothing there. Searching google for "offshift github" brings us to a different github with a [single suspicious repository](https://github.com/offshift-protocol/promo). This has two commits, one where files are uploaded, and one in which the \_\_pycache\_\_ folder is deleted. That folder sounds interesting, so we clone the repository, and checkout the commit where the files were added:

```bash
git clone git@github.com:offshift-protocol/promo.git
cd promo
git checkout dc43c1ac33f767a7d30dbeab123a1c87566e885d
cd __pycache__
```

There, we see one `.pyc` file, which is very likely where the interesting part of this challenge is. To understand it, we use `uncompyle6`:

```bash
pip3 install uncompyle6 --user
uncompyle6 script.cpython-38.pyc > ../../uncompyled.py
```

Now, upon reviewing that file, we see that we have some interesting cipher of sorts that uses XOR and base64 somehow:

```python
import base64
secret = 'https://google.com'
cipher2 = [b'NDE=', b'NTM=', b'NTM=', b'NDk=', b'NTA=', b'MTIz', b'MTEw', b'MTEw', b'MzI=', b'NTE=', b'MzQ=', b'NDE=', b'NDA=', b'NTU=', b'MzY=', b'MTEx', b'NDA=', b'NTA=', b'MTEw', b'NDY=', b'MTI=', b'NDU=', b'MTE2', b'MTIw']
cipher1 = [base64.b64encode(str(ord(i) ^ 65).encode()) for i in secret]
```

From a little deduction, we can guess that the creation of `cipher1` based on `secret` is how the list `cipher2` was developed. Therefore, to decipher that array, we simply need to reverse the list comprehension that generates `cipher1`.

Working from the outside to the inside (to reverse the operations done during enciphering), we will need to first base64 decode each element. Then, we will have to cast it to an int (the output of `ord()`), and then use `chr()` to undo the `ord()` operation. Lastly we must undo the XOR with 65, whcih can be done by simply XORing it again. This can all be accomplished as so:

```python
print(''.join([chr(int(base64.b64decode(x)) ^ 65) for x in cipher2]))
```

From that, we get a URL: https://archive.is/oMl59. That archive is a post on 4chan's /x/ board where the original poster included a link to a [mega.nz file download](https://mega.nz/file/AAdDyIoB#gpj5s9N9-VnbNhSdkJ24Yyq3BWSYimoxanP-p03gQWs). This downloads what appears to be a corrupt "PDF" [file called smashing.pdf], which `file` identifies as "data", indicating that there are no identifiable magic bytes. 

> NOTE: At this point, inference is made that this PDF is encrypted with a repeating key that makes use of the magic bytes to reverse. 

From Wikipedia, we can see that a PDF file should start with `25 50 44 46 2d`, so we perform an XOR to determine what the key that was used to encrypt this PDF was.

```
  25 50 44 46 2d -- PDF Magic Bytes
^ 64 11 05 07 6c -- Start of smashing.pdf
----------------
= 41 41 41 41 41 -- key used to encrypy
```

I would not expect anything less. Therefore, we need to decrypt the whole PDF using this key, and for that, we can use a python script like this one:

```python
with open("smashing.pdf", "rb") as f:
    contents = f.read()

key = b"\x41\x41\x41\x41"
out = b""
for i in range(len(contents)):
    out += bytes([contents[i] ^ key[i % len(key)]])

with open("done_xor.pdf", "wb") as f:
    f.write(out)
```

```bash
file done_xor.pdf
done_xor.pdf: PDF document, version 1.4
```

That's much better, but there's more. When running `strings` on that file, we see references to `flag.txt`, so this could be real steganography. To find out, we use `foremost`:

```bash
dd if=done_xor.pdf | foremost
Processing: stdin
|360+1 records in
360+1 records out
184539 bytes (185 kB, 180 KiB) copied, 0.0017788 s, 104 MB/s
foundat=flag.txtUT
*|
```

Interesting, so we appear to have recovered something. Looking through `foremost`'s [output folder](output), we can see that it sliced a PDF and a Zip archive. Next, we have to unzip that, presumably. Let's give that a shot:

```bash
unzip foremost.zip
Archive:  foremost.zip
[foremost.zip] flag.txt password: 
```

We need a password, and because we do not know it, we are going to have to crack it. To do so, we must build John The Ripper from source (to have access to `zip2john`). For that, I followed [this handy guide](https://hackthestuff.com/article/how-to-install-john-the-ripper-in-linux-and-crack-password). Once installed, it's as easy as:

```bash
zip2john foremost.zip > hashes
john hashes --show
foremost/flag.txt:passwd:flag.txt:foremost::foremost
1 password hash cracked, 0 left
```

Armed with our password `passwd`, we attack the Zip, and get the flag:

```
flag{1t_b33n_A_l0ng_w@y8742}
```

~ Lyell
