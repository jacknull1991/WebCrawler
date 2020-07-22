import requests
import re
from bs4 import BeautifulSoup
import bs4

def getHTMLText(url):
    try:
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        r = requests.get(url, timeout = 30, headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parsePage(ilist, html):
    try:
        print(html[:1000])
        soup = BeautifulSoup(html, "html.parser")
        for sp in soup.find_all("span", class_ = "a-price"):
            print(sp)

    except:
        print('error')

def printGoodsList(ilist):
    print(len(ilist))
    # for i in range(10):
    #     print(ilist[i])

def main():
    query = 'book'
    depth = 2
    start_url = 'https://www.amazon.ca/s?k=' + query
    infoList = []
    try:
        url = start_url
        html = getHTMLText(url)
        parsePage(infoList, html)
    except:
        print('Some error')

    printGoodsList(infoList)

main()
