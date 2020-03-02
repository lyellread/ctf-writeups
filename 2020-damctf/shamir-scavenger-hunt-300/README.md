# Shamir Scavenger Hunt Writeup - 300 Points - Crypto

### Prompt

There is a dam secret in the house. Find enough shares, and reconstruct the secret!

Ex: shamir_memory_mgmt_is_optional

Some shares are hidden around Kearney Hall, some can be found on damctf.xyz, and some can be found via OSINT/recon

Written by Athos and PugofStardoc

Hint 1: See if you can modify the given sage script to reconstruct the secret once you have enough shares.

Hint 2: Check out sections 3.3 and 3.4 of [Mike Rosulek's awesome cryptography book](https://web.engr.oregonstate.edu/~rosulekm/crypto/chap3.pdf). You can tell he is an OSU professor because he has "osu" in his name.

Files: [shamir.sage](2020-damctf/shamir-scavenger-hunt-300/shamir.sage) [shares.txt](2020-damctf/shamir-scavenger-hunt-300/shares.txt)

### Solution

OK, they gave us a free share in the instrucions above: `shamir_memory_mgmt_is_optional`

We first set out to find some of the additional shares referenced, and most were found around Kearney Hall:

```python
"shamir_pineapple_not_pizza",
"shamir_scsi_is_yummy",
"shamir_siLANCE",
"shamir_nvme_is_speedy_boi",
"shamir_i_won't_STANd_by_this",
"shamir_call_the_ambuLANCE",
"shamir_lattices_are_magic",
"shamir_wuddup_highyell",
"shamir_why_are_there_flags",
"shamir_thanos_did_nothing_wrong",
"shamir_crypto_is_hard_pwn_is_life",
"shamir_ppp_has_too_many_wins",
"shamir_wants_sra_not_rsa_but_got_sss",
"shamir_evasion_wen_eta"
```

Additionally, on the twitter of organizer @m0xxz, we found [this tweet](https://twitter.com/m0xxz/status/1231287261112627200?s=20) that containted [this image](2020-damctf/shamir-scavenger-hunt-300/m0x-twitter-image.jpeg). Running through [a stegonography solver](https://futureboy.us/stegano/decinput.html), we find that this contains a share too: `shamir_stack_smashing_detected`

Another organizer's twitter had [a share](https://twitter.com/captainGeech42/status/1231284633788010496): `shamir_segmentation_fault`, the DAMCTF rules page had one `shamir_is_this_in_standard_flag_format?` and the OSUSEC blog also had one `shamir_babytcache101`. 

Now we have a master list of 18-19 of these shares:

```python
shares = ["shamir_stack_smashing_detected",
        "shamir_segmentation_fault",
        "shamir_is_this_in_standard_flag_format?",
        "shamir_babytcache101",
        "shamir_pineapple_not_pizza",
        "shamir_scsi_is_yummy",
        "shamir_siLANCE",
        "shamir_nvme_is_speedy_boi",
        "shamir_i_won't_STANd_by_this",
        "shamir_call_the_ambuLANCE",
        "shamir_lattices_are_magic",
        "shamir_wuddup_highyell",
        "shamir_why_are_there_flags",
        "shamir_thanos_did_nothing_wrong",
        "shamir_crypto_is_hard_pwn_is_life",
        "shamir_ppp_has_too_many_wins",
        "shamir_wants_sra_not_rsa_but_got_sss",
        "shamir_evasion_wen_eta"]
```

Now on to the crypto part. A dive into the textbook indicates that we need to find a polynomial that has points 'at the shares' (both the found ones and the given ones) and the value of f(0) where f is the function of that polynomial will be the flag. Neither of us are crypto wizards, so this rudimentary understanding will have to get us through :)

We noticed that in [shamir.sage](2020-damctf/shamir-scavenger-hunt-300/shamir.sage)

~Lyell Read, Phillip Mestas
