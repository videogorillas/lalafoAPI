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
# tree = make_tree(data['categories'])
# predicted = max_cats(tree, count)

import json
import pprint
import functions

# test

# get data from file
data = json.load(open('validation/jsons/525587834.json', 'rb'))
pprint.pprint(data['categories'], width=160)

print(' ')

# make categories' tree
tree = functions.make_tree(data['categories'])

#pprint.pprint(tree, width=500)

# find two deepest categories with maximum score
predicted = functions.top_predictions(tree, 3)

# output predicted
pprint.pprint(predicted, width=160)
