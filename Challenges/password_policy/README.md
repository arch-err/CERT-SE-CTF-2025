# Solution
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
