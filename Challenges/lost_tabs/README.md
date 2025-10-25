# Solution
1. Export the mail-history (`./lost_tabs.mail_history`) from the pcap (`../../cert-se_ctf2025.pcap`)(Open WS > filter for `tcp.stream eq 8` > Follow TCP Stream > Save as...)
2. Manually copy out the attached base64 blob (`./sessionstore.jsonlz4.b64`), and base64 decode it (`./sessionstore.jsonlz4`)
3. Decompress mozilla lz4 using python (`./decompress.py`)
4. Notice the sus strings at the end of the `cert.se` urls.
5. Develop and run a script (`./get_flag.py`) to extract the sus strings and parse them into a flag.
> The string consists of a number and a character, the number is the index/place in the real flag where the character is, so the section `4[` means that `[` should be in fourth place (`CTF[`)
