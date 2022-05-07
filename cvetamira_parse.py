import pandas as pd
from utils import *
import requests as req
import json

#object_methods = [method_name for method_name in dir(WikiExtractor)
#                  if callable(getattr(WikiExtractor, method_name))]
#print(object_methods)
#WikiExtractor.clean

main_url = "https://cvetamira.ru"
im_descriptions = []
im_names = []
count = 0

# on this site there is nice counting of pictures, so we won't need to parse xml
for i in range(33, 2991):
    url = f'https://cvetamira.ru/art/image/{i}'
    text_parts = reqParseFind(url, 'div', "cvetamira")
    if text_parts is None:
        continue
    try:
        img = reqParseFind(url, 'img', "temp")
    except:
        continue

    im_url = main_url + img['src']
    im_name = im_url.split('/')[-1]
    resp = req.get(im_url, stream=True)
    im_path = f'cvetamira_imgs/{im_name}'
    with open(im_path, 'wb') as f:
        f.write(resp.content)
    print(text_parts.text[:-10].strip())
    print(img)
    im_descriptions.append(text_parts.text[:-10].strip())
    im_names.append(im_name)

    if (count + 1) % 100 == 0:
        data = {'im_name': im_names, 'description': im_descriptions}
        pd.DataFrame.from_dict(data).to_csv('cvetamiraArtistsImDescr.csv', index=False)
        print(f'saved {count} iteration')
    count += 1
    print()

data = {'im_name': im_names, 'description': im_descriptions}
pd.DataFrame.from_dict(data).to_csv('cvetamiraArtistsImDescr.csv', index=False)
