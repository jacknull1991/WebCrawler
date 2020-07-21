import requests
from bs4 import BeautifulSoup

url = "http://python123.io/ws/demo.html"
try:
    r = requests.get(url)
    print(r.status_code)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    print(soup.a.string)

except:
    print("Fail")









