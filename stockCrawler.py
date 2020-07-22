import requests
from bs4 import BeautifulSoup
import traceback
import re

def get_headers():
    return {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
            "cache-control": "max-age=0",
            "dnt": "1",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}

# grab web page content
def getHTMLText(url, code = 'utf-8'):
    try:
        r = requests.get(url, timeout = 30, headers = get_headers)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("Failed to connect to " + url)
        return ""

def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, 'GB2312')
    soup = BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all('a')
    # sXXXXXX | hzXXXXXX
    regex = re.compile(r'[s][hz]\d{6}')
    for a in a_tags:
        try:
            href = a.attrs['href']
            lst.append(regex.findall(href)[0])
        except:
            continue
    

def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, "html.parser")
            stockInfo = soup.find('div', attrs = {'class' : 'stock-bets'})
            # stock name
            name = stockInfo.find_all(attrs = {'class' : 'bets-name'})[0]
            infoDict.update({'股票名称' : name.text.split()[0]})
            # stock data
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                value = valueList[i].text
                infoDict[key] = value
                
            with open(fpath, 'a', encoding = 'utf-8') as f:
                f.write(str(infoDict) + '\n')
                count = count + 1
                print('\rProgress: {:.2f}%'.format(count * 100 / len(lst)), end = '')
        except:
            count = count + 1
            print('\rProgress: {:.2f}%'.format(count * 100 / len(lst)), end = '')
            # traceback.print_exc()
            continue


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = './stockInfo.txt'

    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)

main()






