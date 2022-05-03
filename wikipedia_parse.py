import requests as req
from bs4 import BeautifulSoup
from PIL import Image
import re

#object_methods = [method_name for method_name in dir(WikiExtractor)
#                  if callable(getattr(WikiExtractor, method_name))]
#print(object_methods)
#WikiExtractor.clean

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)

    cleanr = re.compile('\[.*?\]')
    cleantext = re.sub(cleanr, '', cleantext)

    cleantext = cleantext.replace(u'\xa0', u' ')
    cleantext = cleantext.replace('\n', '')
    return cleantext

def reqParseFind(url, findTag):
    resp = req.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = soup.find(id="bodyContent").findAll(findTag)
    return links

def indexByWikiObjTextKey(list, key):
    for index, item in enumerate(list):
        if item.text == key:
            break
    return index

wiki_url = "https://ru.wikipedia.org"
url = "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%BF%D0%BE_%D1%85%D1%83%D0%B4%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC"
url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%BF%D0%BE_%D1%85%D1%83%D0%B4%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC&subcatfrom=%D0%9A%D0%BB%D0%B5%D0%B5%2C+%D0%9F%D0%B0%D1%83%D0%BB%D1%8C%0A%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B+%D0%9F%D0%B0%D1%83%D0%BB%D1%8F+%D0%9A%D0%BB%D0%B5%D0%B5#mw-subcategories"

links = reqParseFind(url, 'a')
links_slice = links[10:15]

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
                text = [cleanhtml(p.text) for p in text]
                imgs = reqParseFind(painting_FULLurl, 'img')
                img_url = 'https:' + imgs[0]['src']
                resp = req.get(img_url, stream=True)
                if len(resp.content) > 3000:
                    im_name = imgs[0]['alt'].replace('.', '').replace(' ', '')
                    with open(f'{im_name}.jpg', 'wb') as f:
                        f.write(resp.content)

                #print(img_url, '\n', len(resp.content))
                #print(imgs[0]['src'][2:])
                #print([img['src'] for img in imgs[0]])
        print()
    break
