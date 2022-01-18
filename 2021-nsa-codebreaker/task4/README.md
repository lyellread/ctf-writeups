# NSACC Task 4 Writeup

## Prompt

A number of OOPS employees fell victim to the same attack, and we need to figure out what's been compromised! Examine the malware more closely to understand what it's doing. Then, use these artifacts to determine which account on the OOPS network has been compromised.

Downloads:

OOPS forensic artifacts [artifacts.zip](artifacts.zip)

Categories: PowerShell, Registry Analysis

Points: 150

## Solve

After reading the script that was found at the end of Task 3 ([pressure_decrypted.ps1](pressure_decrypted.ps1)), we discover that it's main purpose is locating and exfiltrating sensitive data like private keys. For this task, we are given [artifacts.zip](artifacts.zip) which contains several `.ppk` (PuTTY Private Key) and their associated `.pub` Public Keys. We also get [artifacts/NTUSER.DAT](artifacts/NTUSER.DAT), the windows user registry hive, which coincidentally the PowerShell malware [pressure_decrypted.ps1](pressure_decrypted.ps1) reads to determine past connection information. Therefore, we examine the registry keys which the malware also examines. These keys are as follows:

```
\SOFTWARE\SimonTatham\PuTTY\Sessions
\SOFTWARE\Martin Prikryl\WinSCP 2\Sessions
```

Within these, we discover information about several connections:

```
\SOFTWARE\SimonTatham\PuTTY\Sessions
- system: dkr_prd10, user: hypervbot
- system: dkr_prd19, user: tester_04
- system: dkr_prd48, user: tester_08
- system: dkr_prd62, user: tester_09
- system: dkr_prd66, user: tester_01

\SOFTWARE\Martin Prikryl\WinSCP 2\Sessions
- system: dkr_prd10, user: hypervbot
- system: dkr_prd48, user: tester_08
- system: dkr_prd66, user: tester_01
```

Now, we check each key in {`dkr_prd10`, `dkr_prd19`, `dkr_prd48`, `dkr_prd62`, `dkr_prd66`} to see if the `.ppk` file is unencrypted (indicated by `Encryption: none` at the top of the `.ppk` file). We find that only `dkr_prd19.ppk`, `dkr_prd62.ppk` are unencrypted.