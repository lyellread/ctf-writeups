# NSACC Task 6 Writeup

## Prompt

> Now that we've found a malicious artifact, the next step is to understand what it's doing. Identify some characteristics of the communications between the malicious artifact and the LP.

Category: Reverse Engineering

Points: 500

## Solve

Finally into some reverse engineering, we are provided with an obfuscated binary `make` which we have to understand the function of. 

```
file make
	make: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-x86_64.so.1, with debug_info, not stripped
```

We begin statically examining the binary with Ghidra until a sufficient understanding of the function is achieved to move to dynamic examination with `gdb`.

I've included the Ghidra project in this repository ([ghidra-project](../ghidra-project/)), which should include the final state of all the reversing work I did for Tasks 6-9 (`make`) and task 10. 

For Task 6, the only understanding needed was that the function which I have since renamed to `getstring()` (originally obfuscated as `igcqlsqsndznh()`) is responsible for decrypting constant strings stored in the binary. By using `gdb`'s `call` functionality, we can recover the values of each of these strings:

| Hex Argument | Int Argument | String                                                             |
|:-------------|:-------------|:-------------------------------------------------------------------|
| `0x01`       | `1`          | "os"                                                               |
| `0x02`       | `2`          | "version"                                                          |
| `0x03`       | `3`          | "username"                                                         |
| `0x04`       | `4`          | "timestamp"                                                        |
| `0x05`       | `5`          | "unknown"                                                          |
| `0x06`       | `6`          | "/tmp/.gglock"                                                     |
| `0x07`       | `7`          | "/usr/local/src/repo"                                              |
| `0x08`       | `8`          | "pidof git"                                                        |
| `0x09`       | `9`          | "Commit: "                                                         |
| `0x0a`       | `10`         | "Author: "                                                         |
| `0x0b`       | `11`         | "Email: "                                                          |
| `0x0c`       | `12`         | "Time: "                                                           |
| `0x0d`       | `13`         | "No data available"                                                |
| `0x0e`       | `14`         | "ninja"                                                            |
| `0x0f`       | `15`         | "%Y-%m-%d"                                                         |
| `0x10`       | `16`         | "nightly-exfil"                                                    |
| `0x11`       | `17`         | "3.3.4.3-SKP"                                                      |
| `0x12`       | `18`         | `81ef61d1ab0f0ec2322ced1fe29944e47afb076f535692884932cac6f0e86148` |
| `0x13`       | `19`         | "198.51.100.63"                                                    |

Given these values, we can solve Task 6. A nice gentle introduction to the C++ Reverse Engineering that follows.