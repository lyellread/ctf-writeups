# Much Sad

## Prompt

We have received some information that CATAPULT SPIDER has encrypted a client's cat pictures and successfully extorted them for a ransom of 1337 Dogecoin. The client has provided the ransom note, is there any way for you to gather more information about the adversary's online presence?

NOTE: Flags will be easily identifiable by following the format `CS{some_secret_flag_text}`. They must be submitted in full, including the `CS{ and }` parts.

Files: [muchsad.txt](muchsad.txt)

## Solution

First task: understand the file we are provided:

```
+------------------------------------------------------------------------------+
|                                                                              |
|                        ,oc,                                                  |
|   BAD CAT.            ,OOxoo,                                  .cl::         |
|                       ,OOxood,                               .lxxdod,        |
|       VERY CRYPTO!    :OOxoooo.                             'ddddoc:c.       |
|                       :kkxooool.                          .cdddddc:::o.      |
|                       :kkdoooool;'                      ;dxdddoooc:::l;      |
|                       dkdooodddddddl:;,''...         .,odcldoc:::::ccc;      |
|                      .kxdxkkkkkxxdddddddxxdddddoolccldol:lol:::::::colc      |
|                     'dkkkkkkkkkddddoddddxkkkkkxdddooolc:coo::;'',::llld      |
|                 .:dkkkkOOOOOkkxddoooodddxkxkkkxddddoc:::oddl:,.';:looo:      |
|             ':okkkkkkkOO0000Okdooodddddxxxxdxxxxdddddoc:loc;...,codool       |
|           'dkOOOOOOkkkO00000Oxdooddxxkkkkkkxxdddxxxdxxxooc,..';:oddlo.       |
|          ,kOOO0OOkOOOOOO00OOxdooddxOOOOOkkkxxdddxxxxkxxkxolc;cloolclod.      |
|         .kOOOO0Okd:;,cokOOkxdddddxOO0OOOOOkxddddddxkxkkkkkxxdoooollloxk'     |
|         l00KKKK0xl,,.',xkkkkkxxxxkOOOkkOkkkkkxddddddxkkkkkkkkxoool::ldkO'    |
|        '00KXXKK0oo''..ckkkkkkkOkkkkkkxl;'.':oddddddxkkkkkkkkkkkdol::codkO.   |
|        xKKXXK00Oxl;:lxkkkkkkOOkkddoc,'lx:'   ;lddxkkkkkkkxkkkkkxdolclodkO.   |
|       ;KKXXXK0kOOOOOkkkkOOOOOOkkdoc'.'o,.  ..,oxkkkOOOkkkkkkkkkkddoooodxk    |
|       kKXKKKKKOOO00OOO00000OOOkkxddo:;;;'';:okOO0O0000OOOOOOOOOkkxddddddx    |
|      .KKKKKKKKOkxxdxkkkOOO000OkkkxkkkkkxxkkkkkOO0KKKKK0OOOO000OOOkkdddddk.   |
|      xKKKKKKc,''''''';lx00K000OOkkkOOOkkkkkkkkO0KKKKKK0OO0000O000Okkxdkkx    |
|     'KK0KKXx. ..    ...'xKKKK00OOOOO000000000OO0KKKKKKKKKKKKK0OOOOOkxdkko    |
|     xKKKKKXx,...      .,dKXKK00000000KKKKKKKKKKKKKKKKKKKK000OOOOOOkxddxd.    |
|    ,KKKKKXKd'.....  ..,ck00OOOOOOkO0KKKKKKKKKKKKKKKKKK0OOOOkkkkkkkxdddo.     |
|    .KKKKK0xc;,......',cok0O0OOOkkkk0KKKK00000KKK000OOOkkkkkkkkkkkxdddd.      |
|    .KKKKK0dc;,,'''''',:oodxkkkkkkkkkOOOOkOOOOkkkkkkkkkkkkkkkOOkkxdddd,       |
|     0KKKKK0x;'.   ...';lodxxkkkkkkddkkkkkkkkkkkkkkkkkkOOOOOkkOkkkxddc        |
|     xKKKKKK0l;'........';cdolc:;;;:lkkkkkkkkkkkkkkkkOO000OOOOOOkxddd.        |
|     :KKKKK00Oxo:,'',''''...,,,;;:ldxkkkkkkkkkkkkkOkkOOOOOOOOkkkxddd'         |
|      oKKKKK0OOkxlloloooolloooodddxkkkkkkkkkkkkkkkkkkkkkkkOOkkkxddd.          |
|       :KKK00OO0OOkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkO0Okkkkkkkkxddd:            |
|        o0KK00000000OOkkkkkkkkkkkkkkkkkkkkkkkkkkO0000Okkkkkkxdo;.             |
|         'd00000000OOOOOOkkkkkkkkkkkkkkkkkOkOO00Okkkkkkkkkkko,                |
|           .oO00000OOOOOkkkkkkkkkkkkkkkkkkOOOOkOOkkkkkkkkko'                  |
|             .;xO0OOOOOOkkkkkkkkkkkkkkkkkkkkkOkkkkkkkkd:.                     |
|                .lxOOOOkkkkkkkkkkkkkkkkkkkxxxkkkkkd:'                         |
|                   .;okkkkkkkkxxkkdxxddxdxdolc;'..                            |
|                       ...',;::::::;;,'...                                    |
|                                                                              |
|                            MUCH SAD?                                         |
|                      1337 DOGE = 1337 DOGE                                   |
|                DKaHBkfEJKef6r3L1SmouZZcxgkDPPgAoE                            |
|              SUCH EMAIL shibegoodboi@protonmail.com                          |
+------------------------------------------------------------------------------+
```

The description mentions that dogecoin is involved, and the hash `DKaHBkfEJKef6r3L1SmouZZcxgkDPPgAoE` is likely related to that. Therefore, our first order of business is to check that lead out. Not being an expert, that dead-ends [here](https://dogechain.info/address/DKaHBkfEJKef6r3L1SmouZZcxgkDPPgAoE). Next, let's look into that email. 

After some searching, I did a [namechk](namechk.com) search for `shibegoodboi`, which indicated that the twitter account `@shibegoodboi` is in use. Looking towards [that account](https://twitter.com/shibegoodboi), we see a new blockchain address or hash of some sort (`D7sUiD5j5SzeSdsAe2DQYWQgkyMUfNpV2v`) and a github account for "shibefan" (https://github.com/shibefan). That account has the saying "1 DOGE = 1 DOGE" and "shibegoodboi" so we are on the right track, and gives us another blockchain hash of some sort: `D6hRwJbGPxmXGWYfZ7t6S8MRkB7XrBJsLL`.

The first project listed on that github account is [a website](https://github.com/shibefan/shibefan.github.io), which contains an `index.html` file that contains our flag:

```
CS{shibe_good_boi_doge_to_the_moon}
```

~ Lyell