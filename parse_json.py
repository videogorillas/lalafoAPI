# parse json output from lalafoAPI
# output N deepest categories with maximum score on each intermediate node
# usage:
# - either get json data from file
# data = json.load(open('file.json', 'rb'))
# - or get json data from API
# api_url = 'http://podol.videogorillas.com:4244/upload'
# files = {'file': open('file.jpg', 'rb')}
# r = requests.post(api_url, files=files)
# data = r.text
#
# count = 2
# tree = make_tree(data)
# predicted = max_cats(tree, count)

import json
import pprint


# create predicted categories tree from json data
def make_tree(data):
    categories = data['categories']

    tree = {}

    for c in categories:
        path = c['desc'][6:].split('/')
        cur = tree
        for p in path:
            if p not in cur:
                cur[p] = {}
            cur = cur[p]

        cur['attr'] = c
    return tree


# choose `count` categories with max
def max_cat(tree, count):
    res = []
    for node in tree:
        n = tree[node]
        if node != 'attr' and 'attr' in n:
            res.append({'score': n['attr']['score'], 'node': node, 'desc': n['attr']['desc']})

    if len(res) == 0 and 'attr' in tree:
        a = tree['attr']
        return {'score': a['score'], 'desc': a['desc'], 'categoryId': a['categoryId']}

    res.sort(key=lambda k: -k['score'])
    res = res[0: count]
    result = []
    for r in res:
        m = max_cat(tree[r['node']], 1)
        if isinstance(m, list):
            result.append(m[0])
        else:
            result.append(m)
    return result


# test

# get data from file
data = json.load(open('validation/jsons/525707178.json', 'rb'))
pprint.pprint(data['categories'], width=160)

print(' ')

# make categories' tree
tree = make_tree(data)

# find two deepest categories with maximum score
predicted = max_cat(tree, 2)

# output predicted
pprint.pprint(predicted, width=160)
