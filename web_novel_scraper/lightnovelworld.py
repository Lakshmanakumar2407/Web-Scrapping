import requests
from bs4 import BeautifulSoup
import re, os

def main():
    site_url: str = "https://www.lightnovelworld.co/search"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
    }
    fetch(site_url, headers)

def fetch(url, headers):
    session = requests.session()
    # print(session.cookies.get_dict())
    response = session.get(url, headers= headers)
    print(response.status_code)
    
    pattern = r'__cf_chl_f_tk=([^"]+)'

    soup = BeautifulSoup(response.text, 'lxml')
    script_text = soup.find('script')
    match = re.search(pattern, str(script_text))
    cfhl_token = match.group(1)
    print(cfhl_token)

    params = {
        "__cf_chl_tk":cfhl_token
    }
    # searchurl = "https://www.lightnovelworld.com/search/"
    response2 = session.post(url, params= params)
    print(response2.status_code)
    print(BeautifulSoup(response2.text,'lxml').prettify())


if __name__ == '__main__':
    # main()
    url = "https://freewebnovel.com/supreme-harem-god-system.html"
    url2 = "https://novelfull.net/dragon-ball-god-mu.html"
    response = requests.get(url2)
    with open('dump.txt','w', encoding= 'utf-8', newline='') as dump:
        dump.write(BeautifulSoup(response.text, 'lxml').prettify())
    # print(BeautifulSoup(response.text, 'lxml').prettify())

    # d7eM_kK8q2WNW7SGY0UTSuhZb1k.fUw_eDJr21_8S0g-1708410004-0.0-3773
    # 4ioq6lUbDokaI7hKB3tSfRALtUwW4ERT6b6JDAWeznc-1708410224-0.0-3773
    # cf_chl_f_tk