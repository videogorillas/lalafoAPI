import json
import os
import shutil
from PIL import Image
import functions
import re


act = functions.all_cats_tree
for c in act:
    act[c]['title'] = re.sub(r'\d+_', '', act[c]['title']).strip()

# bad image/prediction results
with open('validation_results/bad.txt', 'rb') as f:
    bad = f.readlines()
bad = map(lambda x: x.strip(), bad)

th_size = 150, 100

summary = {'red': {'count': 0, 'html': ''},
           'yellow': {'count': 0, 'html': ''},
           'green': {'count': 0, 'html': ''},
           'blue': {'count': 0, 'html': ''}}

files = [os.path.join(dp, f)
         for dp, dn, filenames in os.walk('validation')
         for f in filenames if f.endswith('.jpg')]

try:
    #shutil.rmtree('validation_results/')
    os.makedirs('validation_results/thumbs/')
except:
    pass

n = 0
for i, fn in enumerate(files):
    id = os.path.basename(fn)
    jsf = 'validation/jsons/' + id.split('.')[0] + '.json'

    print(jsf)

    try:
        data = json.load(open(jsf, 'rb'))
    except:
        continue

    # predicted categories
    tree = functions.make_tree(data['categories'])
    top_predictions = functions.top_predictions(tree, 3)
    main_pred_cat_id = str(top_predictions[0]['categoryId'])

    # make dirs
    d = 'validation_results/'
    d += '_'.join(act[main_pred_cat_id]['title'].split('/')[1:]) + '/'
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
    true_category_id = os.path.dirname(fn).split('/')[-1]
    true_parent_id = act[true_category_id]['path'].split('/')[-2]

    # short report
    short = ''
    for c in top_predictions:
        cid = str(c['categoryId'])
        d = act[cid]['title']
        l = functions.longest_head(d, act[true_category_id]['title'])
        d = d.replace(l, '<span class="hl">' + l + '</span>')
        short += \
            '<tr><td>%s</td><td>%s</td><td>%.02f</td><td><div class="b" style="width:%dpx"</td></tr>' % \
            (cid, d, c['score'], 200 * c['score'] / 100)

    # full report
    full = ''

    # initially
    color = 'red'

    for c in data['categories']:
        cid = str(c['categoryId'])

        # if true category id is among all predictions
        if cid == true_category_id:
            color = 'yellow'

        d = act[cid]['title']
        l = functions.longest_head(d, act[true_category_id]['title'])
        d = d.replace(l, '<span class="hl">' + l + '</span>')

        if cid == true_category_id:
            d = '<strong>' + d + '</strong>'

        full += \
            '<tr><td>%s</td><td>%s</td><td>%.02f</td><td><div class="b" style="width:%dpx"</td></tr>' % \
            (cid, d, c['score'], 200 * c['score'] / 100)

    pred_parent_id = act[main_pred_cat_id]['path'].split('/')[-2]
    if true_parent_id == pred_parent_id:
        color = 'blue'

    if true_category_id == main_pred_cat_id:
        color = 'green'

    summary[color]['count'] += 1

    summary[color]['html'] += \
        '<tr><td>' + id + ' <input type="checkbox" ' + ('checked' if id in bad else '') + '/></td>' + \
        '<td style="background:' + color + '">' + \
        '<a href="../' + cf + '" target="_blank">' + '<img data-original="thumbs/' + id + '"></a></td>' + \
        '<td class="true">' + true_category_id + ' ' + act[true_category_id]['title'] + '</td>' + \
        '<td><table>' + short + '</table>' + \
        '<button class="b-full">Toggle full</button>' + \
        '<table class="full">' + full + '</table>' + \
        '</td></tr>'

    n += 1

colors_tbl = ''
for color in summary:
    c = summary[color]
    colors_tbl += '<tr><td>%s</td><td>%d</td><td>%.02f</td></tr>' % (color, c['count'], 100 * c['count'] / n)

for color in summary:
    c = summary[color]

    html = \
        '<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>' + \
        '<script src="jquery.lazyload.js"></script>' + \
        '<script src="js.js"></script>' + \
        '<style>' + \
        'body{font-size:10px}' + \
        'img{border:0;margin:0 auto;display:block}' + \
        'td{padding:3px 5px;border:#ccc 1px solid;font-size:10px}' + \
        'table{border-collapse:collapse}' + \
        '.true,.full{display:none}' + \
        '.hl{color:red;font-weight:bolder}' + \
        '.b{background-color:green;height:15px;font-size:15px;}' + \
        '</style>'
    html += '<table>' + colors_tbl + '</table>'
    html += '<button id="b-true">Toggle True</button>'
    html += '<table>'
    html += '<tr><th>ID</th><th>Image</th><th class="true">True Cat</th><th>Pred Cats</th></tr>'
    html += summary[color]['html']
    html += '</table>'
    html += '<div class="checked"></div>'

    with open('validation_results/report_' + color + '.html', 'w') as f:
        f.write(html)