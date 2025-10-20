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
