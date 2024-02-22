import os, random, re, time
import requests
from bs4 import BeautifulSoup

def main():
    site_url: str = "https://novelfull.com/absolute-resonance.html"
    base_url_pattern = r'https://novelfull.com'
    base_url = re.match(base_url_pattern, site_url).group()

    list_of_ua = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    ]

    headers = {
        'User-Agent': random.choice(list_of_ua)
    }

    parsed_html = get_html(site_url, headers)
    chapter_list_dict = dict()
    if parsed_html != None:

        novel_name, author_name = get_novel_details(parsed_html)

        url_str, last_page_num = get_pages(parsed_html)


    # chapter_list_dict = get_chapter_list(base_url, url_str, int(last_page_num))

    # creat_doc(novel_name, author_name, chapter_list_dict)



def get_html(url, headers=None, params=None, file=None):
    global soup

    try:
        session = requests.session()
        response = session.get(url, headers=headers, timeout=10)
    except requests.exceptions.Timeout as e:
        print(f'Error occured when fetching the url :{url}')
        print(e)
        return None
    except requests.exceptions.ConnectionError as e:
        print(f'Error occured when fetching the url :{url}')
        print(e)
        return None
    else:
        if response.status_code<400:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        else:
            print(f'Bad response : {response.status_code}')
            return None

def get_novel_details(some_html):
    novel_name = some_html.find('h3', attrs = {'class':'title'}).get_text()
    author_name = (soup.find('div', class_ = 'info')).find('a', attrs={'href':True}).get_text()

    return novel_name, author_name

def get_pages(some_html):
    last_page_num_str = (some_html.find('li', class_ = "last")).find('a')
    pattern  = '\d+'
    match = re.search(pattern, last_page_num_str['href'])
    print(match.group())
    print(last_page_num_str['href'][:-2], last_page_num_str['href'][-2:])
    return last_page_num_str['href'][:-2], last_page_num_str['href'][-2:] # magic nmber bad

def get_chapter_list(home_url: str,page_num_url: str, last_page_num: int):
    print("getting pages...")
    chapter_url_dict = dict()

    for counter in range(last_page_num):
        if counter<=2:
            print(f"Adding Chapters...... {counter}")
            url_to_pass = home_url+page_num_url+str(counter+1)
            some_html = get_html(url_to_pass)

            pattern = r'Chapter \d+'
            chpter = (some_html.find('div', attrs={"class":"col-xs-12", "id":"list-chapter"})).find_all('a', attrs={'href':True, 'title':True})
            
            for chp in chpter:
                match = re.search(pattern, chp.text)
                if match:
                    chapter_url_dict[chp.get_text()] = home_url+chp['href']
        
        # chapter_list_dict = {tag:val for index, (tag,val) in enumerate(chapter_list_dict.items()) if index >4}
    
    return chapter_url_dict

def get_text(url):
    return_html = get_html(url)
    paras = return_html.find_all('p')
    
    return paras[3:-1]

def creat_doc(novel_name, author_name, chapter_list_dict):
    with open(f'{novel_name}.md','w', encoding="utf-8") as novel:
            novel.write(f'# {novel_name} \n\n')
            novel.write(f'*{author_name}* \n\n')
    
    def populate_doc(chapter_list_dict):
        with open(f'{novel_name}.md','a', encoding='utf-8') as novel:
            for key in chapter_list_dict:
                paras = get_text(chapter_list_dict[key])
                novel.write(get_para_as_str(paras, key))

    populate_doc(chapter_list_dict)

    return None

def get_para_as_str(list_of_paras, chapter_title):
    str_to_return = ""
    str_to_return += ("## " + chapter_title)
    str_to_return += '\n\n'
    for para in list_of_paras:
        str_to_return += para.get_text()
        str_to_return += "\n\n"
    
    return str_to_return

if __name__ == '__main__':
    main()
    
