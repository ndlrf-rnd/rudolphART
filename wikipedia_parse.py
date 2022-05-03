import requests as req
from bs4 import BeautifulSoup
import pickle

wiki_url = "https://ru.wikipedia.org"
url = "https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%BF%D0%BE_%D1%85%D1%83%D0%B4%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC"
url = "https://ru.wikipedia.org/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B_%D0%BF%D0%BE_%D1%85%D1%83%D0%B4%D0%BE%D0%B6%D0%BD%D0%B8%D0%BA%D0%B0%D0%BC&subcatfrom=%D0%9A%D0%BB%D0%B5%D0%B5%2C+%D0%9F%D0%B0%D1%83%D0%BB%D1%8C%0A%D0%9A%D0%B0%D1%80%D1%82%D0%B8%D0%BD%D1%8B+%D0%9F%D0%B0%D1%83%D0%BB%D1%8F+%D0%9A%D0%BB%D0%B5%D0%B5#mw-subcategories"

def reqParseFind(url, findTag):
    resp = req.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = soup.findAll(findTag)
    return links

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
            start_urls = [url.text for url in paintingsLinks[:5]]
            end_urls = [url.text for url in paintingsLinks[-60:]]
            nonUsefulLinksTexts = start_urls + end_urls
            print(nonUsefulLinksTexts)
            with open('nonUsefulWikiLinksTexts.pickle', 'wb') as f:
                pickle.dump(nonUsefulLinksTexts, f)
            break
    break
