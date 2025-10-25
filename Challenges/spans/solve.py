#!/usr/bin/env python

with open("./index.html", "r") as filep:
   file = filep.readlines()

# print(file)

for line in file:
    if "<span></span>" in line:
        num_of_spans = len(list(filter(None, line.strip().split(" "))))
    elif "span:nth-of-type(" in line:
        lighter_spans = sorted(line.strip().replace("span:nth-of-type(", "").replace(")", "").split(", "))
# print(num_of_spans)
# print(lighter_spans)
result = ""
for i in range(num_of_spans):
    if str(i) in lighter_spans:
        result += "0"
        continue
    result += "1"

print(result)
