# Solution
1. Extract the mail-traffic: `tshark -r ../../cert-se_ctf2025.pcap -qz follow,tcp,ascii,10 > tcp10.txt; dos2unix tcp10.txt`
2. Extract the b64 blob and decode it, put it in `SD_Card.img`
3. Perform some basic analysis ([`info.md`](./info.md))
4. Discover the deleted file "`mystery.jpg`", interesting!! (`fls ./SD_Card.img`)
5. Attempt to recover files using sleuthkit (`tsk_recover ./SD_Card.img ./tsk_recover -e`)
6. Notice we got a `mystery.jpg`, but the file looks corrupt, there are some extra bytes in places we don't want 'em...
7. `ffmpeg` is pretty accepting of fucked up files, try to read the file with ffmpeg and write it to a new file: `ffmpeg -i ./tsk_recover/mystery.jpg mystery.jpg`
8. Read the flag written out in the restored [`mystery.jpg`](./mystery.jpg) image -> [`flag.txt`](./flag.txt)
