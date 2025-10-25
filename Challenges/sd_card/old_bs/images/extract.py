#!/usr/bin/env python

import os

for fil in os.listdir("./"):
    if ".png" not in fil: continue

    # os.rmdir(f"./{fil.replace(".png", "")}")
    # os.mkdir(f"./{fil.replace(".png", "")}")

    print(os.system(f"binwalk {fil} | grep file"))
