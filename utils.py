import re
import requests as req
from bs4 import BeautifulSoup

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)

    cleanr = re.compile('\[.*?\]')
    cleantext = re.sub(cleanr, '', cleantext)

    cleantext = cleantext.replace(u'\xa0', u' ')
    cleantext = cleantext.replace('\n', '')
    return cleantext

def reqParseFind(url, findTag, source="wikipedia"):
    resp = req.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    if source == "wikipedia":
        links = soup.find(id="bodyContent").findAll(findTag)
    elif source == "opisanie-kartin":
        links = soup.find(findTag, class_ = "entry-content").findAll('p')
    return links

def indexByWikiObjTextKey(list, key):
    for index, item in enumerate(list):
        if item.text == key:
            break
    return index
