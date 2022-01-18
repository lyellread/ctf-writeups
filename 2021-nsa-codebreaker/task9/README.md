# NSACC Task 9 Writeup

## Prompt

Now that we're able to register, let's send some commands! Use the knowledge and material from previous tasks to identify other clients that have registered with the LP.

Categories: Protocol Analysis, Software Development

Points: 3500

## Solve

Given how misguided I was trying to solve Task 8, I pre-wrote this whole task speculatively while waiting for my brute force runs to work. It might be that, or it might be that Task 9 is just an easier challenge overall, but the workload felt quite low for 3500 points. Sandwiched between 8 and 10, that's a welcome break. 

On to solving it, I opted for a more complete approach. I wrote a little library in the file [packet_bytes.py](packet_bytes.py). This library can generate a client to server command string based on a list of parameters and arguments. This is called from [connect.py](connect.py), a script written intentionally to take advantage of the functionality the server grants the client to arbitrarily print files on the remote, and print directory listings as well. Very cool. 

How did I discover this functionality? Well, I dumped and pretty-printed the contents of each session's communications using [decode.py](decode.py) and all the session (or stream) information in [streams/](streams). Using this, I could establish the understanding that the client issues the requests to the server, not the other way around:

```
Decoded for Stream 0
-----------------------------------
# Init Message
To Server: 1b4e81973d00000200023d080010948c87e58e22449d882173657851cce8e02293f2
cmd(init), uuid(948c87e58e22449d882173657851cce8), 

# Code 0 - essentially ACK
From Server: 1b4e81973d28000400000000e02293f2
code(<0x00><0x00><0x00><0x00>), 

# Response to ACK?
To Server: 1b4e81973d00000200033d080010948c87e58e22449d882173657851cce8e02293f2
cmd(init_complete), uuid(948c87e58e22449d882173657851cce8), 

# Created a Dir for our client 948c87e58e22449d882173657851cce8
From Server: 1b4e81973d14003c2f746d702f656e64706f696e74732f39343863383765352d386532322d343439642d383832312d3733363537383531636365382f7461736b696e6700e02293f2
dirname(/tmp/endpoints/948c87e5-8e22-449d-8821-73657851cce8/tasking<0x00>), 

# Request directory listing
To Server: 1b4e81973d00000200043d080010948c87e58e22449d882173657851cce83d14003c2f746d702f656e64706f696e74732f39343863383765352d386532322d343439642d383832312d3733363537383531636365382f7461736b696e6700e02293f2
cmd(tasking_ready), uuid(948c87e58e22449d882173657851cce8), dirname(/tmp/endpoints/948c87e5-8e22-449d-8821-73657851cce8/tasking<0x00>), 

# Server provides directory listing
From Server: 1b4e81973d1800077461736b2d32003d1800077461736b2d3100e02293f2
add_task(task-2<0x00>), add_task(task-1<0x00>), 

# Request file contents for task-2
To Server: 1b4e81973d00000200053d080010948c87e58e22449d882173657851cce83d14003c2f746d702f656e64706f696e74732f39343863383765352d386532322d343439642d383832312d3733363537383531636365382f7461736b696e67003d1c00077461736b2d3200e02293f2
cmd(next_task_request), uuid(948c87e58e22449d882173657851cce8), dirname(/tmp/endpoints/948c87e5-8e22-449d-8821-73657851cce8/tasking<0x00>), command/filename(task-2<0x00>), 

# Server responds with file contents
From Server: 1b4e81973d20001952554e3a207368613173756d202f6574632f7061737377640ae02293f2
result/contents(RUN: sha1sum /etc/passwd\n), 

...
```

Once arbitrary file read was achieved, the SSH private key to the `lpuser` account was printed, and SSH access was gained. From here, all that is required is listing the /tmp/endpoints/ directory to get access to all the UUIDs registered with the LP. This can even be done without an SSH key.