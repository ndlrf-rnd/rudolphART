import pandas as pd
import re
from time import sleep
from utils import *

#object_methods = [method_name for method_name in dir(WikiExtractor)
#                  if callable(getattr(WikiExtractor, method_name))]
#print(object_methods)
#WikiExtractor.clean

wiki_url = "https://ru.wikipedia.org"
#url = "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%BF%D0%BE_%D1%85%D1%83%D0%B4%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC"
#url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%BF%D0%BE_%D1%85%D1%83%D0%B4%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC&subcatfrom=%D0%9A%D0%BB%D0%B5%D0%B5%2C+%D0%9F%D0%B0%D1%83%D0%BB%D1%8C%0A%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B+%D0%9F%D0%B0%D1%83%D0%BB%D1%8F+%D0%9A%D0%BB%D0%B5%D0%B5#mw-subcategories"
url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%BF%D0%BE_%D1%85%D1%83%D0%B4%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC&subcatfrom=%D0%A1%D0%B8%D0%BD%D1%8C%D0%B5%D0%B8-%D0%9C%D0%B5%D1%80%D1%88%D0%B5%0A%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B+%D0%9F%D0%B0%D0%BB%D0%B0+%D0%A1%D0%B8%D0%BD%D1%8C%D0%B5%D0%B8-%D0%9C%D0%B5%D1%80%D1%88%D0%B5#mw-subcategories"

links = reqParseFind(url, 'a')
links_slice = links[4:-6]

#print([a.text for a in links_slice])

count = 0
im_descriptions = []
im_names = []
for artist_link in links_slice:
    artist_FULLurl = url + artist_link['href']
    paintingsListLinks = reqParseFind(artist_FULLurl, 'a')
    
    #print(paintingsListLinks)
    for paintingListLink in paintingsListLinks:
        #print(painting_link.text)
        if 'Картины ' in paintingListLink.text:
            #print(painting_link)
            paintings_FULLurl = wiki_url + paintingListLink['href']
            paintingsLinks = reqParseFind(paintings_FULLurl, 'a')
            
            categ_index = indexByWikiObjTextKey(paintingsLinks, 'Категории')
            paintingsLinks = paintingsLinks[:categ_index]
            filteredPaintingLinks = []

            for paintingLink in paintingsLinks:
                if paintingLink['href'].find("/wiki/") != -1\
                    and "Список" not in paintingLink.text and "Медиафайлы" not in paintingLink.text:
                    filteredPaintingLinks.append(paintingLink)

            for paintingLink in filteredPaintingLinks:
                painting_FULLurl = wiki_url + paintingLink['href']
                text = reqParseFind(painting_FULLurl, 'p')
                sleep(0.3)
                text = ' '.join([cleanhtml(p.text) for p in text[:6]])
                imgs = reqParseFind(painting_FULLurl, 'img')
                sleep(0.3)
                img_url = 'https:' + imgs[0]['src']
                resp = req.get(img_url, stream=True)

                print()
                print(resp)
                print(img_url)
                print()

                if len(resp.content) > 2000:
                    im_name = imgs[0]['alt'].replace('.', '').replace(' ', '')[:50]
                    im_path = f'imgs/{im_name}.jpg'
                    with open(im_path, 'wb') as f:
                        f.write(resp.content)

                    im_descriptions.append(text)
                    im_names.append(im_name)
                    if (count + 1) % 100 == 0:
                        data = {'im_name': im_names, 'description': im_descriptions}
                        pd.DataFrame.from_dict(data).to_csv('wikiArtistsImDescr.csv', index=False)
                        print(f'saved {count} iteration')
                    count += 1
                sleep(0.3)

                #print(img_url, '\n', len(resp.content))
                #print(imgs[0]['src'][2:])
                #print([img['src'] for img in imgs[0]])
