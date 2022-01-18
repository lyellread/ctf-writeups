# NSACC Task 7 Writeup

## Prompt

With the information provided, PANIC worked with OOPS to revert their Docker image to a build prior to the compromise. Both companies are implementing additional checks to prevent a similar attack in the future.

Meanwhile, NSA's Cybersecurity Collaboration Center is working with DC3 to put together a Cybersecurity Advisory (CSA) for the rest of the DIB. DC3 has requested additional details about the techniques, tools, and targets of the cyber actor.

To get a better understanding of the techniques being used, we need to be able to connect to the listening post. Using the knowledge and material from previous tasks, analyze the protocol clients use to communicate with the LP. Our analysts believe the protocol includes an initial crypt negotiation followed by a series of client-generated requests, which the LP responds to. Provide the plaintext a client would send to initialize a new session with the provided UUID.

Downloads:

Victim ID to use in initialization message [victim_id](victim_id)

Category: Protocol Analysis

Points: 500

## Solve

And the reverse engineering continues on the Ghidra project at [ghidra-project](../ghidra-project/). For task 7, we continue statically reversing the `make` binary to better understand it's function. Along the way we come upon a function which is called as follows:

```c
socket = make_socket(lp_ip,lp_port);
if (-1 < socket) {
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string((basic_string *)&msg_to_send);
    ret = crypt_neg_send_pubkey(socket,&msg_to_send);
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string((basic_string<char,std::char_traits<char>,std::allocator<char>> *)&msg_to_send);
    if (ret == 0) {
      std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string((basic_string *)&uuid_string);
      build_init_message(&msg_to_send,&uuid_string);
      std::vector<std--__cxx11--,std--allocator<std--__cxx11-->>::push_back(&messages,(value_type *)&msg_to_send);
```

Shorthanding the C++ cruft that Ghidra forces on us, we can rewrite the above snippet as:

```c
socket = make_socket(lp_ip,lp_port);
if (-1 < socket) {
    alloc_basic_string((basic_string *)&msg_to_send);
    ret = crypt_neg_send_pubkey(socket,&msg_to_send);
    free_basic_string(&msg_to_send);
    if (ret == 0) {
      alloc_basic_string((basic_string *)&uuid_string);
      build_init_message(&msg_to_send,&uuid_string);
      message_vector.push_back(&messages,&msg_to_send);
```

We can see that the function I preemptively named `build_init_message()` is called at the right time and in the right way to be the constructor of the first message in the sequence. Therefore, we examine it's decompilation. This snippet has had the C++ cruft removed as above.

```c
string * build_init_message(string *__return_storage_ptr__,string *uuid)
{
    size_t length;
    long in_FS_OFFSET;
    string *message;
    string magic_start;
    string cmd_param;
    string cmd_length;
    string cmd_data;
    string uuid_param;
    string uuid_length;
    string magic_end;
    long stack_canary;

    stack_canary = *(long *)(in_FS_OFFSET + 0x28);

    htons_string_32(&magic_start,MAGIC_START);
    htons_string_16(&cmd_param,PARAM_CMD);
    htons_string_16(&cmd_length,2);
    htons_string_16(&cmd_data,COMMAND_INIT);
    htons_string_16(&uuid_param,PARAM_UUID);
    length = length(uuid);
    htons_string_16(&uuid_length,length);
    htons_string_32(&magic_end,MAGIC_END);

    append(&temp1,&magic_start,&cmd_param);
    append(&temp2,&temp1,&cmd_length);
    append(&temp3,&temp2,&cmd_data);
    append(&temp4,&temp3,&uuid_param);
    append(&temp5,&temp4,&uuid_length);
    append(&temp6,&temp5,uuid);
    append(__return_storage_ptr__,&temp6,&magic_end);

    if (stack_canary != *(long *)(in_FS_OFFSET + 0x28)) {
    __stack_chk_fail();
    }
    return __return_storage_ptr__;
}
```

This function sets the byte order to network byte order using `htons`. Then it concatenates the arguments together in order to generate what will be referred to as the init message. An example init message for the given UUID is shown below:

```
1b4e8197 3d00 0002 0002 3d08 0010 34d61721414d4f77baf079e1a262ec34 e02293f2
   |      |    |    |    |    |                |                       |
  magic   |    |   cmd   |   uuid length      uuid                   magic end
    param cmd  |       uuid param
             cmdlen
```

This solves Task 7, but this knowledge will be used through the next tasks extensively.