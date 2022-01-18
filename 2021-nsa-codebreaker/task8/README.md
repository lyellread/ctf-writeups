# NSACC Task 8 Writeup

## Prompt

Knowing the contents we'd send to initialize a new session is good progress. The next step is to uncover additional details about the protocol.

We suspect the Docker malware was specifically tailored to PANIC's image and written exclusively to steal their source code. Given that, it seems likely that the malware only contains a subset of the communications protocol supported by the LP. Our network capture does appear to have communications from other malware variants. If we could decrypt those communications, then we could analyze the underlying plaintext to recover additional details about the protocol.

As a reminder, our analysts believe the protocol includes an initial crypt negotiation followed by a series of client-generated requests, which the LP responds to.

Decrypt the other sessions captured in the PCAP. Provide the UUIDs of each of the clients associated with the DIB that registered with the LP.

Category: Cryptanalysis

Points: 3000

## Solve

To solve Task 8, we begin with more reverse engineering. Note that the Ghidra project I worked on is available in it's finished state here: [ghidra-project](../ghidra-project/). This entails discovering and understanding the cryptography of this scheme. This entails understanding both the sequence of messages sent, as well as the cryptographic primitives and keys used in each of those messages. I'll cover each of these in their own section to separate them.

### Message Sequence

From the decompilation of the function I've named `malware_main()`, we can see the general structure of the program and how it makes calls to send and receive messages. This looks a little like the following, truncated for readability:

```c
get_session_key(&session_key,username,malware_version,time.tv_sec);
socket = make_socket(lp_ip,lp_port);
if (-1 < socket) {
    ret = crypt_neg_send_pubkey(socket,&msg_to_send);
    if (ret == 0) {
        build_init_message(&msg_to_send,&uuid_string);
        vector::push_back(&messages,&msg_to_send);

        //pseudocode generated by me, decomp is bad with iterating over this vector
        for (message in messages){
            encrypt_build_msg(&msg_to_send,&uuid_string,buf,buf_len);
            vector::push_back(&ciphertexts,&msg_to_send);
        }

        //pseudocode generated by me, decomp is bad with iterating over this vector
        for (ciphertext in ciphertexts){
            ret = sock_send(socket,ciphertext,ciphertext_len);
            ret = socket_response(socket,&msg_to_send);
            if (ret != 0) break;
        }
    }
}
```

This shows us how all the major function interact to generate, send and receive the messages to/from the LP. Next, the interesting functions are `get_session_key()`, `crypt_neg_send_pubkey()` and `encrypt_build_msg()`. Let's examine each in a simplified manner.

#### `get_session_key()`

This function is quite intimidating at first glance. It has SHA contexts, weird functions filled with bytewise manipulation, and other weird things. The key here is to not get scared, and instead to start making assumptions. For example, we see that at the end of the function, the hash context seems to be written into a buffer of size 32, indicating this is a 32 byte / 256 bit hash. From there it's just a small assumption away to assume SHA256. See for yourself:

```c
string * get_session_key(string *__return_storage_ptr__,char *username,char *version,
                        time_t timestamp)

{
  //many locals of no import here
  BYTE buf [32];

  to_lower_case(&lowecaseUser,username);

  //normally this would not be included but it tells us the version number length
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string((char *)&versionShort,(ulong)version,(allocator *)0x7);
  std::allocator<char>::~allocator(&local_2a9);

  session_key_unhashed = std::operator<<(abStack456,(basic_string *)&lowecaseUser);
  session_key_unhashed = std::operator<<(session_key_unhashed,"+");
  session_key_unhashed = std::operator<<(session_key_unhashed,(basic_string *)&versionShort);
  session_key_unhashed = std::operator<<(session_key_unhashed,"+");

  instantiate_hash_ctx?(&hash_ctx);
  len = length(session_key_unhashed);
  data = (BYTE *)session_key_unhashed
                           ();
  make_hash(&hash_ctx,data,len);
  session_key = hash_to_buf(&hash_ctx,buf);
}
```

While this is a very rough translation of a quite complicated and confusing function, it gives the essentials for understanding how the session key is derived by the client. This is the beating heart of Task 8, and it's all downhill once this function is understood. Essentially, this creates the session key as follows:

```
|| denotes concatenation

session_key = sha256(username.lower || + || version[:7] || + || timestamp)
```

#### `crypt_neg_send_pubkey()`

```c
int crypt_neg_send_pubkey(int sock,string *fp)

{
  //locals were here
  
  result = -1;
  server_pk = (char *)0x0;

  //open public key box here
  crypto_box_curve25519xsalsa20poly1305_ref_keypair(&client_public_key);
  server_pk = getstring(0x12);
  get_random_bytes(&nonce,0x18);

  //encryption takes place here
  crypto_box_curve25519xsalsa20poly1305_ref(&ciphertext,fp,&nonce,&server_public_key);
  ciphertext_len = length(ciphertext);
  fp_len = length(fp);
  bodyLen = fp_len + ciphertext_len; //ciphertext includes nonce

  //magical header added here (discussed below)
  make_length_header(&header,bodyLen);

  //message is assembled
  string_concat(&temp1,&client_public_key,&header);
  string_concat(&temp2,&temp1,&nonce);
  string_concat(&payload,&temp2,&ciphertext);

  //message is sent
  bufLen = length(payload);
  vbuf = payload
  result = sock_send(sock,vbuf,bufLen);
  return result;
}
```

the function `crypt_neg_send_pubkey()` sends the server the following message:

```
E_pub(key, nonce, plaintext) denotes encryption of plaintext with key and nonce using elliptic curve / public key encryption
|| denotes concatenation

client_pubkey || header || nonce || E_pub(server_pubkey, nonce, fingerprint)
```

An interesting note is that it seems as though the client public key is sent in a separate packet in the captures, though it's unclear whether this actually makes any functional difference.

What's this header value? Well, consider that the client must share the payload length with the server so that the server can process the data it's receiving. If the protocol were to do this in the open, we could clearly see this in the network capture we are given, and already have *some* information about the scheme. Therefore, it's "encrypted" using some nasty-looking code in the `make_length_header()` function. That function can be summarized with the following snipped of python:

```py
def generate_length_header(l):
    # Get random 2-byte value
    a = random.randint(0, 65535).to_bytes(2, "big")
    i = int(a.hex(), 16)
    r = l - i + 0x10000
    # Convert to bytes from int after math
    b = r.to_bytes(2, "big")

    return a + b
```

#### `encrypt_build_msg()`

The last function of interest is the `encrypt_build_msg()` function. Let's examine this one now:

```c
string * encrypt_build_msg(string *__return_storage_ptr__,string *session_key,void *message_plaintext,size_t size)

{
  //locals were here
  
  get_random_bytes(&nonce,0x18);

  //missing code which either Ghidra cannot process or happens elsewhere.
  //    a secretbox is instantiated with "sessionkey" as the key.

  //encryption
  crypto_secretbox_xsalsa20poly1305_ref(&ciphertext,&message,&nonce);
  ciphertext_length = length(ciphertext);

  //some variables in here were provided in the symbols.
  //you really think I would mix camel case and snake case?
  bodyLen = ciphertext_length + 0x18;
  make_length_header(&length_headerStr,bodyLen);

  //build message
  string_concat(&header_and_nonce,&length_headerStr,&nonce);
  string_concat(__return_storage_ptr__,&header_and_nonce,&ciphertext);

  return __return_storage_ptr__;
}

```

This looks pretty cut and dry (except for the instantiation of the secretbox which must take place somewhere else I did not locate or Ghidra cannot decompile it). What we have in this function is shared key cryptography based on what is called "session key". Essentially, this function takes the session key derived earlier, and uses it to encrypt a given message as follows:

```
E_sk(key, plaintext) denotes encryption of plaintext with shared secret key `key`
|| denotes concatenation

header || nonce || E_sk(session_key, message_n)
```

### Cryptography... Or something

Now, we understand that there are to different types of encryption going on here, and it makes sense. We have to be able to crack this somehow, and for all intents and purposes we cannot crack properly used public key encryption as it features here. Therefore, it's on to that shared / session key. Essentially, if we observe that the client sends the following messages to the server, we will be able to reason about how the whole protocol works, and what we can and cannot crack:

```
E_pub(key, nonce, plaintext) denotes encryption of plaintext with key and nonce using elliptic curve / public key encryption
E_sk(key, plaintext) denotes encryption of plaintext with shared secret key `key`
|| denotes concatenation

Message 0: 
pubkey || header || nonce || E_pub(pubkey, nonce, fingerprint)

Init and all later messages:
session_key = sha256(username.lower || + || version[:7] || + || timestamp)
header || nonce || E_sk(session_key, message_n)
```

This shows us exactly what we want to see. The client first sends over a fingerprint, which is composed as follows:

```
fingerprint = b64(username=<username>),b64(version=<version>),b64(os=<os>),b64(timestamp=<timestamp>)
```

Based on this, it's safe to assume that the secure transmission of the fingerprint is to allow for the serve to independently derive it's own identical session key as the client, using the client's data present in the fingerprint. Therefore, given that we have ruled out brute forcing the public key cryptography, we must be forcing the values which make up the session key in order to crack sessions.

### Let's Brute Force!

The last step in this task is to develop a script and start bruteforcing these session keys. I've done so in [bruteforce_shared_key.py](bruteforce_shared_key.py). Essentially, this makes use of the `pynacl` library to encrypt and decrypt, and mimics the client as closely as possible. From there, it multiprocesses usernames against a set `offset` from the time that message appeared in [capture.pcap](capture.pcap). 

It's that easy. And it can be solved on a `t2.micro` if you have the sensibility to narrow the parameters enough. In case you (like me) don't, I've listed the solve in terms of [bruteforce_shared_key.py](bruteforce_shared_key.py) below:

```
python3 bruteforce_shared_key.py wordlists/4-cirt.txt 5
python3 bruteforce_shared_key.py wordlists/8-names.txt 5
```

This generates the following session keys:

| Username   | Version   | Timestamp    |
|:-----------|:----------|:-------------|
| `root`     | `3.3.4.3` | `1615897652` |
| `vcsrv`    | `1.4.9.0` | `1615897720` |
| `anisa`    | `1.5.9.1` | `1615897622` |
| `ngan`     | `0.0.1.0` | `1615897642` |
| `rozanna`  | `1.7.6.6` | `1615897723` |
| `xiaofeng` | `0.9.2.2` | `1615897683` |