'''
scrapper for animedaily.net

TO DO
1. ask user for the webpage link
2. ask how many chapters to scrape
3. store the scrapped data to csv or text
4. Try making the code modular by using functions
'''

import time
import requests
from bs4 import BeautifulSoup

def timer(some_func):
    def wrapper():
        Start_time = time.time()
        some_func()
        End_time = time.time()
        print(f'Time took to execute: {End_time - Start_time}')
    return wrapper
    

@timer
def main():
    # Url and intital request
    url = input(f'Enter the url to be scraped: ')
    response = requests.get(url).text

    # Parsing through beautiful soup
    soup = BeautifulSoup(response,'lxml')

    # Getting Novel Name...
    Novel_name = soup.find('h3',class_ = 'title', attrs= {'itemprop':'name'}).text

    # geting the hidden novel id
    in_put = soup.find('input', {'id': 'id_post'})
    id = in_put['value']

    # getting the last available page
    last_page = soup.find('a', attrs={'data-page':True, 'title':True})
    last_page = last_page['data-page']

    # establishing new session
    session = requests.session()

    # Created for storing parsed chapter list 
    ugly_chapter_list = []

    # parsing through all pagination
    for pag_no in range(int(last_page)):
        
        # payload passed along with post request
        files = {
            'action':"tw_ajax",
            'type':"pagination",
            'id': id,
            'page':pag_no+1
        }

        chapter_list_response = session.post('https://animedaily.net/wp-admin/admin-ajax.php', data = files, timeout=3).text

        soup1 = BeautifulSoup(chapter_list_response,'lxml')
        # with open('dummy1.html','w',newline='') as dummy:
        #     dummy.write(soup1.prettify())

        # Extracting chapter list form parsed html and storing it in ugly_chapter_list
        a_link = soup1.find_all('a', attrs= {'href':True, 'title':True, 'data-page':False})
        for a in a_link:
            ugly_chapter_list.append(a['href'])

    # Removing unwanted characters from the string
    clean_chapter_list = []
    for chapter in ugly_chapter_list:
        temp_chap = chapter.split('"')[1]
        clean_chapter_list.append(temp_chap.replace("\\",''))

    # Creating new file for storing extracted text
    new_file = open(f'{Novel_name}.md','w')
    new_file.write('# '+ Novel_name)
    new_file.write('\n\n\n')
    new_file.close()

    no_of_chap_to_scrape = int(input(f'There are {len(clean_chapter_list)} chapter, How many do you want to scrape? : '))

    for chapter in clean_chapter_list[:(no_of_chap_to_scrape)]:
        # print(chapter)
        # Sending requests for each chapter and extracting required data
        r = requests.get(chapter).text
        soup2 = BeautifulSoup(r,'lxml')

        chapter_title = soup2.find('a',class_='chapter-title').text

        # Extracting all the paragraphs and storing it in a temporary list
        temp_list = []
        for p in soup2.find_all('p'):
            temp_list.append(p.text)

        # Removing last three lines of filler
        text_list = temp_list[:-3]

        with open(f'{Novel_name}.md','a', encoding='utf-8') as doc:
            doc.write('## '+ chapter_title)  
            doc.write('\n\n')
            for line in text_list:
                doc.write(line)
                doc.write('\n\n')
            doc.write('\n\n\n')

        # print(temp_list,len(temp_list))

def get_page_and_link():
    pass

def create_novel_file():
    pass

if __name__ == '__main__':
    main()