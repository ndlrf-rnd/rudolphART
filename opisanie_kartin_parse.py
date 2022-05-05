import pandas as pd
from utils import *
import requests as req

#object_methods = [method_name for method_name in dir(WikiExtractor)
#                  if callable(getattr(WikiExtractor, method_name))]
#print(object_methods)
#WikiExtractor.clean

sitemap_url = "https://opisanie-kartin.ru/post-sitemap.xml"

#links = reqParseFind(sitemap_url, 'a')
#links_slice = links[4:-6]

#print([a.text for a in links_slice])

import xmltodict
import json

resp = req.get(sitemap_url)
#print(resp.text)
doc = xmltodict.parse(resp.text)

#json = json.dumps(doc)
print(doc)
