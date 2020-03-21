# RSAPWN Writeup

### Prompt

We must train the next generation of hackers.

`nc challenges.tamuctf.com 8573`

### Solution

It looks like this just asks us to find the two "big prime" factors of the number provided, and return them. [Athos' script](exploit.py) does exactly that:

```bash
python3 ./exploit.py 
[+] Opening connection to challenges.tamuctf.com on port 8573: Done
b'We must train future hackers to break RSA quickly. Here is how this will work.\nI will multiply together two big primes (<= 10000000), give you the result,\nand you must reply to me in less than two seconds telling me what primes I\nmultiplied.\n\nPress enter when you are ready.\n'
num b'99981300873901'
9999083 9999047
b'Good job :)'
b'gigem{g00d_job_yOu_h4aaxx0rrR}'
b''
```

Easy.

```
gigem{g00d_job_yOu_h4aaxx0rrR}
```

~Athos, Lyell Read
