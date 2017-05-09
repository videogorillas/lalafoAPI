import json
import re
import pprint


cats = {}

with open('testdata/tree.txt') as f:
    txt = f.readlines()

for i, l in enumerate(txt):
    rs = re.sub(r'[^\d/]', '', l).split('/')
    ls = l.strip().split('/')
    for j in range(0, len(rs)):
        cats[int(rs[j])] = {'title': '/'.join(ls[0: j+1]), 'path': '/'.join(rs[0: j+1])}

with open('tree.json', 'w') as f:
    json.dump(cats, f)

pprint.pprint(cats, width=300)
