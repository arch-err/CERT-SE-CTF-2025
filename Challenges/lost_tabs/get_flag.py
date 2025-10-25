#!/usr/bin/env python
import subprocess

command = "cat ./sessionstore.json | jq | grep url | grep cert.se"
urls = subprocess.check_output(["bash", "-c", command]).decode().split("\n")
clean_urls = []

for url in urls:
    if url == '': continue
    clean_urls.append(url.replace('              "url": "https://cert.se/#', '').replace('",', ''))

full_string = ''.join(clean_urls)

groups = []


num = ""
for i in range(len(full_string)):
    c = full_string[i]
    if c in "0123456789":
        num += c
    else:
        groups.append((num, c))
        num = ""
print(''.join(c for _, c in sorted(groups, key=lambda x: int(x[0]))))
