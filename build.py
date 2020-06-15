import urllib.request
import os
import json
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
    
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
    else:
        if module['name'].lower() in names:
            print('WARNING: Duplicate module name:', url)

        names.add(module['name'].lower())

        # Upgrade legacy fields
        if 'options' in module:
            if 'niceName' in module['options']:
                module['options']['cliName'] = module['options']['niceName']
                del module['options']['niceName']

        if 'category' in module:
            if 'keywords' not in module:
                module['keywords'] = [module['category']]
            else:
                module['keywords'].append(module['category'])
            del module['category']
        else:
            if 'keywords' not in module:
                module['keywords'] = ['network']

        result.append(module)
  except:
    print(url)

# Sort by name
def guiname(x):
    if 'options' in x:
        if 'guiName' in x['options']:
            return strip_tags(x['options']['guiName'])
        if 'cliName' in x['options']:
            return strip_tags(x['options']['cliName'])
    return x['name']
    
result = sorted(result, key = lambda x: guiname(x).lower())

with open('modulelist.json', 'w') as fh:
    json.dump(result, fh)

print(len(result), 'mods listed!')
print(sum(1 for x in result if 'network' in x['keywords']), 'network mods listed!')
print(sum(1 for x in result if 'client' in x['keywords']), 'client mods listed!')
