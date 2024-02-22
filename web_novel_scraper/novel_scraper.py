import time, os, random, re
import requests
from bs4 import BeautifulSoup

class NovelScraper:

    list_of_ua = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    ]

    def __init__(self, url, headers=None) :
        self.site_url = url
        if headers is None:
            self.headers = {
                'User-Agent':random.choice(NovelScraper.list_of_ua)
            }
        else:
            self.headers = headers

    def get_html(self):
        try:
            session = requests.session()
            response = session.get(self.site_url, headers=self.headers, timeout=10)
        except requests.exceptions.Timeout as e:
            print(f'Error occured when fetching the url :{self.site_url}')
            print(e)
            return None
        except requests.exceptions.ConnectionError as e:
            print(f'Error occured when fetching the url :{self.site_url}')
            print(e)
            return None
        else:
            if response.status_code<400:
                soup = BeautifulSoup(response.text, 'lxml')
                return soup
            else:
                print(f'Bad response : {response.status_code}')
                return None
            
class NovelFull(NovelScraper):
    def __init__(self, url, header=None):
        super().__init__(url, header)

    def get_pages(soup_object):
        last_page_num_str = (soup_object.find('li', class_ = "last")).find('a')
        # pattern  = '\d+'
        # match = re.search(pattern, last_page_num_str['href'])
        # print(match.group())
        # print(last_page_num_str['href'][:-2], last_page_num_str['href'][-2:])
        return last_page_num_str['href'][:-2], last_page_num_str['href'][-2:]


