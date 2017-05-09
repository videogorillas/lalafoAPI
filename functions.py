import json

# tree of all categories
# we need it to unambiguously detect categories having same name
all_cats_tree = json.load(open('tree.json', 'rb'))


def longest_head(s1, s2):
    m = min(len(s1), len(s2))
    i = 0
    while i < m and s1[i] == s2[i]:
        i += 1
    return s1[0: i]


# create predicted categories tree from json data
def make_tree(categories):

    tree = {}

    for c in categories:
        path = all_cats_tree[str(c['categoryId'])]['path'].split('/')[1:]
        cur = tree
        for p in path:
            if p not in cur:
                cur[p] = {}
            cur = cur[p]

        cur['attr'] = c
    return tree


# choose `count` categories with max
def top_predictions(tree, count):
    res = []
    for node in tree:
        n = tree[node]
        if node != 'attr' and 'attr' in n:
            res.append({'score': n['attr']['score'], 'node': node})

    if len(res) == 0 and 'attr' in tree:
        a = tree['attr']
        return {'score': a['score'], 'categoryId': a['categoryId']}

    res.sort(key=lambda k: -k['score'])
    res = res[0: count]
    result = []
    for r in res:
        m = top_predictions(tree[r['node']], 1)
        if isinstance(m, list):
            result.append(m[0])
        else:
            result.append(m)
    return result
