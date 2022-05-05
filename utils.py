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
