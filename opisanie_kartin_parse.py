import pandas as pd
from utils import *
import requests as req
import xmltodict
import json

#object_methods = [method_name for method_name in dir(WikiExtractor)
#                  if callable(getattr(WikiExtractor, method_name))]
#print(object_methods)
#WikiExtractor.clean

sitemap_url = "https://opisanie-kartin.ru/post-sitemap.xml"

#links = reqParseFind(sitemap_url, 'a')
#links_slice = links[4:-6]

#print([a.text for a in links_slice])


resp = req.get(sitemap_url)
#print(resp.text)
doc = xmltodict.parse(resp.text)
urls = doc['urlset']['url']

#json = json.dumps(doc)
im_descriptions = []
im_names = []
count = 0
for url in urls:
    try:
        text_parts = reqParseFind(url['loc'], 'div', "opisanie-kartin")
    except:
        continue
    description = ''
    for p in text_parts:
        description += p.text
        description += '\n'
    try:
        img_url = url['image:image']['image:loc']
        im_name = url['image:image']['image:title']
    except:
        try:
            img_url = url['image:image'][0]['image:loc']
            im_name = url['image:image'][0]['image:title']
        except:
            continue
        continue
    print()
    im_descriptions.append(description)
    print(url['image:image'])
    im_names.append(im_name)
    resp = req.get(img_url, stream=True)
    im_path = f'opisanie_kartin_images/{im_name}.jpg'
    with open(im_path, 'wb') as f:
        f.write(resp.content)
    if (count + 1) % 100 == 0:
        data = {'im_name': im_names, 'description': im_descriptions}
        pd.DataFrame.from_dict(data).to_csv('opisKartinArtistsImDescr.csv', index=False)
        print(f'saved {count} iteration')
    count += 1
    print()

data = {'im_name': im_names, 'description': im_descriptions}
pd.DataFrame.from_dict(data).to_csv('opisKartinArtistsImDescr.csv', index=False)

