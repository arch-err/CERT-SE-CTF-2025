![logo](logo.png)

# CERT-SE CTF 2025
- https://www.cert.se/2025/10/antar-du-var-utmaning.html

## Description
As in previous years CERT-SE has put together a CTF during the cyber security month. This year we do not have a theme but you are going to get to know a very interesting character during the competition. The challenge is open to anyone with an interest in IT security regardless of the level of expertise.

In the .zip file below is a network dump (PCAP) that contains a total of ten flags. All of these have the format "`ctf[string]`" or "`CTF[STRING]`". Everything you need in order to find the flags is included in the network dump and can be solved without connection to the internet. You will not find any clues in any online references. However, free external tools can be useful.

When you have found as many flags as you can, please email them to us along with a description of how you solved the various tasks. It does not matter if the flags submitted are upper or lower case. Email cert@cert.se, with “CTF2025” as the subject of the email.

Please note, we will only accept one response per person. Make sure to find as many flags as possible before submitting. The last day to submit your answer is 31 October 2025.


# Challenges

**Flags:** (3/9)

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
1.

***Flag: `<++>`***


## <name>
1.

***Flag: `<++>`***


## <name>
1.

***Flag: `<++>`***


## <name>
1.

***Flag: `<++>`***


## <name>
1.

***Flag: `<++>`***


## <name>
1.

***Flag: `<++>`***
