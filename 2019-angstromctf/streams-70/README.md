# Streams Writeup - 70 Points

### Prompt

White noise is useful whether you are trying to sleep, relaxing, or concentrating on writing papers. Find some natural white noise [here](https://streams.2019.chall.actf.co/).

Note: The flag is all lowercase and follows the standard format (e.g. actf{example_flag})

Author: ctfhaxor

Hint: Are you sure that's an mp4 file? What's inside the file?

### Solution

First, we deduced some information about the challenge by reading the description. "The flag is all lowercase" implies that we will be constructing it letter by letter, possibly from audio. First thing to check out is the video on the linked website - just river sounds. 

We then proceeded to inspect the website - the HTML looks pretty standard, and I decided to leave player.js alone and come back to it if we failed to find a solution (would be more of a web challenge at that point). Under the 'Network' tab, we see that there appear to be two streams:
```
chunk-stream0-0000*.m4s chunks initiated by init-stream0.m4s
chunk-stream1-0000*.m4s chunks initiated by init-stream1.m4s
```
![Image](https://github.com/lyellread/ctf-writeups/blob/master/angstromctf-2019/streams-70/network-inspection.JPG)

In addition there are two attempts to get a file called stream.mp4 (one that has a status of 206 - partial content, and one 200 - complete)... interesting. We got the file uwing the "Request URL":
```bash
$wget https://streams.2019.chall.actf.co/video/stream.mp4
```
... and ran
```bash
$file stream.mp4
stream.mp4: XML 1.0 document, ASCII text
```
That's interesting... Let's open that in an editor. The XML reads as follows (cleaned up for conciseness):
```xml
<?xml version="1.0" encoding="utf-8"?>

		<AdaptationSet id="0" contentType="video" segmentAlignment="true" bitstreamSwitching="true" frameRate="30/1" lang="und">
			<Representation id="0" mimeType="video/mp4" codecs="avc1.64001f" bandwidth="278539187" width="1280" height="720" frameRate="30/1">
				...
			</Representation>
		</AdaptationSet>
		<AdaptationSet id="1" contentType="audio" segmentAlignment="true" bitstreamSwitching="true" lang="eng">
			<Representation id="1" mimeType="audio/mp4" codecs="mp4a.40.2" bandwidth="128000" audioSamplingRate="44100">
				<AudioChannelConfiguration schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011" value="2" />
				...
			</Representation>
		</AdaptationSet>
		<AdaptationSet id="2" contentType="audio" segmentAlignment="true" bitstreamSwitching="true" lang="und">
			<Representation id="2" mimeType="audio/mp4" codecs="mp4a.40.2" bandwidth="48000" audioSamplingRate="8000">
				<AudioChannelConfiguration schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011" value="1" />
				...
			</Representation>
		</AdaptationSet>
	</Period>
</MPD>
```	
Notice that there are actually 3 streams: 0: mp4 video, 1, 2: mp4 audio. Our hunch that some audio will contain our flag is looking good, but how to get this last audio file? To ensure that we know how this process of 'getting' a channel looks and works, we try it on a channel we know to exist: channel 0: mp4 video. 

From our examination of the files required for the page, we know there are 4 chunks needed, and an init file. We know their names too.
```bash
$wget https://streams.2019.chall.actf.co/video/init-stream0.m4s
$wget https://streams.2019.chall.actf.co/video/chunk-stream0-00001.m4s
...
$wget https://streams.2019.chall.actf.co/video/chunk-stream0-00004.m4s
$ls
chunk-stream0-00001.m4s
chunk-stream0-00002.m4s
chunk-stream0-00003.m4s
chunk-stream0-00004.m4s
init-stream0.m4s
```	
Now that we have all our m4s chunks, we can concattenate them into an mp4 file:
```bash
$cat init-stream0.m4s $(ls -vx chunk-stream0-*.m4s) > stream0.mp4
```
That file plays the video of the brook that is on the site! Now onto grabbing the unknown audio stream. We need:

	- init file for stream2
	- chunks 1..n of stream2

...and because we know naming conventions, we can guess that those files will be called:

	- init-stream2.m4s
	- chunk-stream2-0000x.m4s | x in 1..n
	
Lets go try to grab that init file:
```bash
$wget https://streams.2019.chall.actf.co/video/init-stream2.m4s
‘init-stream2.m4s’ saved [741/741] 
```
It exists! We're go to get the chunks now, but how do we know how many to grab? What I did was to keep wget-ing the next one while the size of the file was reasonably large:
```bash	
$wget https://streams.2019.chall.actf.co/video/chunk-stream2-00001.m4s
‘chunk-stream2-00001.m4s’ saved [32629/32629]
```	
... rinse repeat:
```bash
$ls -lah 
32K  chunk-stream2-00001.m4s
31K  chunk-stream2-00002.m4s
32K  chunk-stream2-00003.m4s
33K  chunk-stream2-00004.m4s
32K  chunk-stream2-00005.m4s
33K  chunk-stream2-00006.m4s
9.7K chunk-stream2-00007.m4s
1.5K chunk-stream2-00008.m4s
883  chunk-stream2-00009.m4s
883  chunk-stream2-00010.m4s
883  chunk-stream2-00011.m4s
741  init-stream2.m4s
```	
Notice how the sizes drop off at the end? Chunks 9, 10, 11 are not even fetching chunks anymore, they are getting the HTML for the site. We can delete those, and keep 1..8.

Now we turn those good chunks into a mp4 file:
```bash
$cat init-stream2.m4s $(ls -vx chunk-stream2-*.m4s) > stream2.mp4
```	
Listening to this file makes it obvious that morse code is at play, so off to the [online audio file to text (via morse) converter]( https://morsecode.scphillips.com/labs/audio-decoder-adaptive/). There we upload the mp4, and get this result:
```
ACTF<KN>F#45H-15-B34D-10N9-11V3-M#39-D45H)
```
Well that looks ok... but what are those '#'? running it again cleans some of this up:
```
ACTF<KN>F145H-15-B34D-10N9-11V3-MP39-D45H)
```
Let's try to understand what it is saying. "flash is bead long live mpeg-dash". They likely meant 'dead' not 'bead' so let's fix that and give that flag a try:
```
actf{f145h_15_d34d_10n9_11v3_mp39_d45h}
```
Nice!

~Lyell Read
