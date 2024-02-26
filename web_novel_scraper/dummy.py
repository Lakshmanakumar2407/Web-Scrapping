import requests, re, time
from bs4 import BeautifulSoup

site_url = "https://novelbin.com/b/coiling-dragon/chapter-749"
# site_url = re.sub(r'\\/','/', site_url)
# print(site_url)
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
params = {
    'novelId':'coiling-dragon'
}
session = requests.session()
for i in range(100):
    site_url =f"https://novelbin.com/b/coiling-dragon/chapter-{740+i}"
    response = session.get(site_url, headers=headers)
    print(response.url, response.status_code)
    time.sleep(2)
    if response.status_code == 429:
        print(response.headers)
        break
soup = BeautifulSoup(response.text, 'lxml')
# with open('reference.html','w',encoding='utf-8', newline='') as refer:
#     refer.write(soup.prettify())

# paras = soup.find_all('p')[1:]
# for para in paras:
#     print(para.get_text())
