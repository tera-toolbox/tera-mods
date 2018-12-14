import urllib.request
import os
import json

# Download all module.json files from the list
lines = open('modulelist.txt').readlines()
result = []
names = set()
for url in lines:
  try:
    myreq = urllib.request.urlopen(url)
    mydata = myreq.read()
    
    module = json.loads(mydata.decode('utf-8'))
    if 'name' not in module:
        print('No name specified:', url)
    elif module['name'].lower() in names:
        print('Duplicate module name:', url)
    else:
        names.add(module['name'].lower())
        result.append(module)
  except:
    print(url)

# Sort by name
result = sorted(result, key = lambda x: x['name'])

with open('modulelist.json', 'w') as fh:
    json.dump(result, fh)
    