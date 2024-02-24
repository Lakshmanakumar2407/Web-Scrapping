import requests, re
from bs4 import BeautifulSoup

site_url = "https://novelbin.com/b/coiling-dragon"
# site_url = re.sub(r'\\/','/', site_url)
# print(site_url)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

session = requests.session()
response = session.get(site_url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
with open('reference.html','w',encoding='utf-8', newline='') as refer:
    refer.write(soup.prettify())

# author = soup.find('a', attrs={'href':True, 'itemprop':'author','title':True}).get_text()
# print(author)
