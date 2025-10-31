![logo](logo.png)

# CERT-SE CTF 2025
- https://www.cert.se/2025/10/antar-du-var-utmaning.html

## Description
As in previous years CERT-SE has put together a CTF during the cyber security month. This year we do not have a theme but you are going to get to know a very interesting character during the competition. The challenge is open to anyone with an interest in IT security regardless of the level of expertise.

In the .zip file below is a network dump (PCAP) that contains a total of ten flags. All of these have the format "`ctf[string]`" or "`CTF[STRING]`". Everything you need in order to find the flags is included in the network dump and can be solved without connection to the internet. You will not find any clues in any online references. However, free external tools can be useful.

When you have found as many flags as you can, please email them to us along with a description of how you solved the various tasks. It does not matter if the flags submitted are upper or lower case. Email cert@cert.se, with “CTF2025” as the subject of the email.

Please note, we will only accept one response per person. Make sure to find as many flags as possible before submitting. The last day to submit your answer is 31 October 2025.


# Challenges

**Flags:** (8/9)

## strings_or_cat
1. `strings *.pcap | rg -i CTF'\['`

***Flag: `ctf[strings_or_cat?]`***


## hexahue
1. Find the [modified cert-se logo](./CERT-SE.jpg) in the pcap-file
> Open pcap in WS > File > Export Objects > HTTP
2. Recognize that it's hexahue-encoded/uses the hexahue-cipher.
> I've seen this before
3. Search the internet for a key, [this](./key.jpg) will work!
4. Decode manually (tedious, but it works)

***Flag: `ctf[couleurshexadecimales]`***


## UDP Keylogger
```python
#!/usr/bin/env python solve.py | grep -oP "ctf\[.*\]" | tee flag.txt #
from scapy.all import rdpcap, UDP
import base64

packets = rdpcap('../../cert-se_ctf2025.pcap')
data = []

for pkt in packets:
    if pkt.haslayer(UDP):
        payload = bytes(pkt[UDP].payload)
        if payload:
            try:
                decoded = base64.b64decode(payload)
                data.append(decoded.decode('utf-8', errors='ignore'))
            except:
                pass

print(''.join(data))
```

***Flag: `ctf[keylog_over_udp]`***


## Monstrum Piscis Tres
1. First of all: extract the base64 blob, decode it, and spend countless friggin hours both with and without claude trying to analyze the audio file, without discovering anything useful. Graphing the audio in every way there is, analyzing signals in about a thousand different ways, and generally just spend hours banging your head into a wall with this damn audio.
2. Send the file to a collegue (non ctf:er) as a joke, only to have him instantly respond with *"speed it up and reverse the audio, there is something there. Awful beeping sound though..."*
3. Sooooo, just reverse the audio (`sox audio.wav reverse.wav reverse`) and remove some of the annoying beep (`ffmpeg -i audio.wav -af "equalizer=f=1000:t=q:w=2:g=-30" -c:a pcm_s16le audio_debeep.wav`).
4. Transcribe the audio file by ear -> `INKEMW2GJFJUQXJA`
5. `echo INKEMW2GJFJUQXJA | base32 -d`

***Flag: `CTF[FISH]`***


## ctf.txt
1. Read the file [`ctf.txt`](./ctf.txt) directly in the pcap
2. Follow the instructions

***Flag: `ctf[a guess]`***


## Lost Tabs
1. Export the mail-history (`./lost_tabs.mail_history`) from the pcap (`../../cert-se_ctf2025.pcap`)(Open WS > filter for `tcp.stream eq 8` > Follow TCP Stream > Save as...)
2. Manually copy out the attached base64 blob (`./sessionstore.jsonlz4.b64`), and base64 decode it (`./sessionstore.jsonlz4`)
3. Decompress mozilla lz4 using python (`./decompress.py`)
4. Notice the sus strings at the end of the `cert.se` urls.
5. Develop and run a script (`./get_flag.py`) to extract the sus strings and parse them into a flag.
> The string consists of a number and a character, the number is the index/place in the real flag where the character is, so the section `4[` means that `[` should be in fourth place (`CTF[`)

***Flag: `ctf[resurrection]`***


## Password Policy
1. Notice the ftp traffic in the [pcap](../../cert-se_ctf2025.pcap), extract it (or at least view it)
2. Save the string in `PASS 983e3...`, might be interesting later.
3. Extract the file [`passwd_policy.txt`](./passwd_policy.txt) and read it.
4. The string after `PASS` looks like an md5-hash. I bet that's the hash of a password in [`rockyou.txt`](https://github.com/zacheller/rockyou), wrapped in `CTF[]` or `ctf[]` according to the passwd_policy.
```bash
awk '{print "ctf[" $0 "]"}' "$rockyou" > ./wordlist.txt
awk '{print "CTF[" $0 "]"}' "$rockyou" >> ./wordlist.txt

hashcat -m 0 -a 0 983e3a1fbb4232fff96282ab9a37f89a ./wordlist.txt
```
5. Hashcat finds the [flag](./flag.txt)

***Flag: `ctf[cutenessie4eva]`***


## Spans
***Sigh...***
Well, this was a tough nut to crack! I know that I may be looking in the completely wrong direction, that is a possibility. Since this CTF doesn't follow the standard "Jeopardy" format that CTFs usually have, there is no clear indication as to where the challenges actually are. However, I have looked through the `pcap` thoroughly, and since I found 8 flags from all of the other leads, this HTML-span-thingy is either a red herring or the final challenge. Soo, I started digging, and digging... aaaand digging some more. I've had multiple friends and colleagues sanity-check me on this one, but I just can't find a flag from this thing. Looking at the lighter and darker spans as 1s and 0s, I've tried binary, bacon, morse, EVERYTHING!! Mapping it as a 64x64 grid and scanning it as some type of code? Nah... Staring at it endlessly to see if I can piece together visually. Nope, I'm done with this now. To be fair, this is an extremely obscure challenge, and I've got other CTFs to play too... *\*cough\* huntress... \*cough\**

***Flag: `not found`***


## SD Card
1. Extract the mail-traffic: `tshark -r ../../cert-se_ctf2025.pcap -qz follow,tcp,ascii,10 > tcp10.txt; dos2unix tcp10.txt`
2. Extract the b64 blob and decode it, put it in `SD_Card.img`
3. Perform some basic analysis ([`info.md`](./info.md))
4. Discover the deleted file "`mystery.jpg`", interesting!! (`fls ./SD_Card.img`)
5. Attempt to recover files using sleuthkit (`tsk_recover ./SD_Card.img ./tsk_recover -e`)
6. Notice we got a `mystery.jpg`, but the file looks corrupt, there are some extra bytes in places we don't want 'em...
7. `ffmpeg` is pretty accepting of fucked up files, try to read the file with ffmpeg and write it to a new file: `ffmpeg -i ./tsk_recover/mystery.jpg mystery.jpg`
8. Read the flag written out in the restored [`mystery.jpg`](./mystery.jpg) image -> [`flag.txt`](./flag.txt)

***Flag: `ctf[im_really_alive]`***
