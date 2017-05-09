import os, requests

files = [os.path.join(dp, f)
         for dp, dn, filenames in os.walk('validation')
         for f in filenames if f.endswith('.jpg')]

api_url = 'http://podol.videogorillas.com:4244/upload'

for i, fn in enumerate(files):

    js = 'validation/jsons/' + os.path.basename(fn).split('.')[0] + '.json'
    print(i, js)

    if os.path.isfile(js):
        continue

    files = {'file': open(fn, 'rb')}

    r = requests.post(api_url, files=files)

    with open(js, 'w') as f:
        f.write(r.text)

