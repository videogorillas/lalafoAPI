import json
import os
import shutil
from PIL import Image


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


th_size = 100, 100

cats = {'2094': {'title': 'Job/Resumes CVs/Construction', 'parent_id': 2075},
        '1467': {'title': 'Children s Item/Kids clothes shoes/Jeans Trousers', 'parent_id': 1463},
        '1614': {'title': 'Vehicles/Used cars/Infiniti', 'parent_id': 1502}}

summary = {'red': 0, 'yellow': 0, 'green': 0, 'blue': 0}

files = [os.path.join(dp, f)
         for dp, dn, filenames in os.walk('validation')
         for f in filenames if f.endswith('.jpg')]

try:
    #shutil.rmtree('validation_results/')
    os.makedirs('validation_results/thumbs/')
except:
    pass

html = '<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>' + \
        '<script src="jquery.lazyload.js"></script>' + \
       '<script src="js.js"></script>' + \
       '<style>body{font-size:10px}' + \
       'img{border:0;}td{padding:5px;border:#ccc 1px solid;font-size:10px}' + \
       'table{border-collapse:collapse}</style>'
html += '<table>'
html += '<tr><th>ID</th><th>Image</th><th>Orig Cat</th><th>Pred Cats</th></tr>'

for i, fn in enumerate(files):
    id = os.path.basename(fn)
    jsf = 'validation/jsons/' + id.split('.')[0] + '.json'

    print(jsf)

    try:
        data = json.load(open(jsf, 'rb'))
    except:
        continue

    tree = make_tree(data)
    pred_cats = max_cat(tree, 2)
    print(pred_cats)
    first_cat = pred_cats[0]

    d = 'validation_results/' + str(first_cat['categoryId']) + '_'
    d += '_'.join(first_cat['desc'].split('/')[1:]) + '/'
    if not os.path.isdir(d):
        os.makedirs(d)

    cf = d + id
    try:
        shutil.copyfile(fn, cf)
    except:
        pass

    # thumbnail
    thf = 'validation_results/thumbs/' + id
    if not os.path.isfile(thf):
        im = Image.open(cf)
        im.thumbnail(th_size)
        im.save(thf, "JPEG")

    # ground true
    orig_cat = os.path.dirname(fn).split('/')[-1]

    s = []
    color = 'red'
    for j, c in enumerate(data['categories']):
        if c['categoryId'] == int(orig_cat):
            color = 'yellow'
        if j == 0:
            s.append('<strong>' + str(c['categoryId']) + ' ' + c['desc'] + '</strong>')
        else:
            s.append(str(c['categoryId']) + ' ' + c['desc'])

    parent = "/".join(first_cat['desc'].split('/')[:-1])
    parent_id = 0
    for c in data['categories']:
        if c['desc'] == parent:
            parent_id = c['categoryId']

    if int(parent_id) == cats[orig_cat]['parent_id']:
        color = 'blue'

    if first_cat['categoryId'] == int(orig_cat):
        color = 'green'

    summary[color] += 1

    if color == 'red':
        html += '<tr><td>' + id + '</td>' + \
                '<td style="background:' + color + '">' + \
                '<a href="../' + cf + '" target="_blank">' + '<img data-original="thumbs/' + id + '"></a></td>' + \
                '<td>' + orig_cat + ' ' + cats[orig_cat]['title'] + '</td>' + \
                '<td>' + '<br>'.join(s) + '</td></tr>'

html += '</table>'

html += '<table>'
for color, count in summary.iteritems():
    html += '<tr><td>' + color + '</td><td>' + str(count) + '</td></tr>'
html += '</table>'

with open('validation_results/report.html', 'w') as f:
    f.write(html)
