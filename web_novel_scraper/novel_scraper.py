import random, re, subprocess
import requests
from bs4 import BeautifulSoup


class NovelScraper:
    """
    This is base template for other classes.
    None of the methods here are for user use
    """
    list_of_ua = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    ]

    def __init__(self, url,
                 selected_option: str = None,
                 starting_number: int = 1, 
                 ending_number: int =None, 
                 output_format: str = None,
                 headers=None) :
        '''
        This is a constructor method for the baseclass
        Contains some of the required attributes some which are passed by the user otherwise, initialised for internal usage
        '''
        self.site_url: str = url
        self.selected_option: str = selected_option
        self.starting_number: int = starting_number
        self.ending_number: int = ending_number
        self.output_format: str = output_format
        self.headers: dict = headers or {'User-Agent':random.choice(NovelScraper.list_of_ua)}
        self.session = None
        self.soup = None
        self.payload: dict = None
        self.chapter_url_dict: dict = None

    def _create_session(self):
        self.session = requests.session()
        return self.session
    
    def _get_html_response(self, method = 'GET', url: str = None):
        try:
            if self.session is None:
                self._create_session()

            url = url or self.site_url
            response = self.session.request(method, url, headers=self.headers, data= self.payload, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'Error occured when fetching the url :{self.site_url}')
            print(e)
            return None
        else:
            if response.status_code<400:
                self.soup = BeautifulSoup(response.text, 'lxml')
                return self.soup
            else:
                print(f'Bad response : {response.status_code}')
                return None

    def get_novel_details(self):
        self._get_html_response()

        self.novel_name: str = None
        self.author: str = None

    def _touch_doc(self):
        with open(f'{self.novel_name}.md','w', encoding="utf-8") as novel:
            novel.write(f'# {self.novel_name} \n\n')
            novel.write(f'*{self.author}* \n\n')
        
        self.chapter_name: str = None
        self.content: list = None

        return None
    
    def create_md(self):
        self.get_chapter_list()
        self._touch_doc()

    def _write_doc(self):
        with open(f'{self.novel_name}.md','a', encoding="utf-8") as novel:
            novel.write(f'## {self.chapter_name}\n\n')
            for content in self.content:
                novel.write(content.get_text())
                novel.write('\n')
            novel.write("\n\n")

    def _convert_md(self):
        input_file = f"{self.novel_name}.md"
        output_file = f"{self.novel_name}.{self.output_format}"

        pandoc_command = ['pandoc', input_file, '-o', output_file, "--metadata", "title="+self.novel_name]

        try:
            subprocess.run(pandoc_command, check= True)
            print("Your File is ready")
        except subprocess.CalledProcessError as e:
            print(f'Error - {e}')

    def get_final(self):
        self.create_md()
        if self.output_format is not None:
            self._convert_md()

    @staticmethod
    def inclusive_range(start, stop):
        return range(start, stop+1)
    

class ChapterListExhausted(Exception):
    pass


class NovelFull(NovelScraper):

    def __init__(self, url: str, 
                 starting_number: int= 1, 
                 ending_number: int = None, 
                 output_format: str = None, 
                 header: dict = None):
        super().__init__(url, starting_number, ending_number, output_format, header)
        self.last_page_num = None
        self.base_url = r'https://novelfull.com'
        self.page_search_url = None

    def get_novel_details(self) -> tuple[str, str]:
        super().get_novel_details()

        self.novel_name = self.soup.find('h3', attrs = {'class':'title'}).get_text()
        self.author = (self.soup.find('div', class_ = 'info')).find('a', attrs={'href':True}).get_text()

        return (self.novel_name, self.author)

    def _get_pages(self):
        self.get_novel_details()

        last_page_link = (self.soup.find('li', class_ = "last")).find('a')
        self.page_search_url = last_page_link['href'][:-2]
        self.last_page_num = int(last_page_link['href'][-2:])
        
        return self.page_search_url, self.last_page_num
    
    def get_chapter_list(self) -> dict:
        self._get_pages()
        self.chapter_url_dict = dict()

        print("getting pages...")

        for counter in NovelScraper.inclusive_range(1, self.last_page_num):
            print(f"fetching Chapters from page - {counter}")
            self.site_url = self.base_url+self.page_search_url+str(counter)
            try:
                self._fetch_chapter_url_from_page()
            except ChapterListExhausted:
                break
        
        return self.chapter_url_dict

    def _fetch_chapter_url_from_page(self): 

        self.soup = self._get_html_response()

        pattern = r'Chapter (\d+)'
        chpter = (self.soup.find('div', attrs={"class":"col-xs-12", "id":"list-chapter"})).find_all('a', attrs={'href':True, 'title':True})
        
        for chp in chpter:
            match = re.search(pattern, chp.text)
            chapter_num = int(match.group(1))
            if self.ending_number is not None:
                if chapter_num in NovelScraper.inclusive_range(self.starting_number, self.ending_number):
                    self.chapter_url_dict[chp.get_text()] = self.base_url+chp['href']
                if chapter_num == self.ending_number:
                    raise ChapterListExhausted
            else:
                self.chapter_url_dict[chp.get_text()] = self.base_url+chp['href']

    def create_md(self):
        super().create_md()

        for chp_name, link in self.chapter_url_dict.items():
            self.site_url = link
            self.soup = self._get_html_response()
            self.chapter_name = chp_name
            self.content = self.soup.find_all('p')[3:-1]
            self._write_doc()


class AnimeDaily(NovelScraper):
    def __init__(self, url, 
                 starting_number: int=1, 
                 ending_number: int=None, 
                 output_format: str=None, 
                 headers=None):
        super().__init__(url, starting_number, ending_number, output_format, headers)
        self.secret_id = None
        self.last_page_num = None
        self.page_search_url: str = "https://animedaily.net/wp-admin/admin-ajax.php"

    def get_novel_details(self) -> tuple[str, str]:
        super().get_novel_details()

        self.novel_name = self.soup.find('h3',attrs = {'class':'title'}).get_text()
        pattern = r'(.*) Novel'
        match = re.match(pattern,self.novel_name)
        self.novel_name = match.group(1)

        self.author = self.soup.find('a', attrs={'href':True, 'itemprop':'author','title':True}).get_text()

        return self.novel_name, self.author

    def _get_pages(self):
        self.last_page_num = self.soup.find('a', attrs={'data-page':True, 'title':True})
        self.last_page_num = int(self.last_page_num['data-page'])

        return self.last_page_num

    def _get_secred_id(self):
        self.secret_id = self.soup.find('input', {'id': 'id_post'})['value']

        return self.secret_id
    
    def _populate_payload(self, page_num: int):
        self.payload = {
            'action':"tw_ajax",
            'type':"pagination",
            'id': self.secret_id,
            'page':page_num
        }

        return self.payload

    def get_chapter_list(self) -> dict:
        self.get_novel_details()
        self._get_pages()
        self._get_secred_id()
        self.chapter_url_dict = dict()
        
        for page_num in NovelScraper.inclusive_range(1, self.last_page_num):
            self._populate_payload(page_num)
            self._get_html_response(method='POST', url= self.page_search_url)

            print(f'fetching chapters from page - {page_num}')
            try:
                if page_num<6: self._fetch_chapter_url_from_page()
            except ChapterListExhausted:
                break

        return self.chapter_url_dict
    
    def _fetch_chapter_url_from_page(self):
        chapters_links = self.soup.find_all('a', attrs= {'href':True, 'title':True, 'data-page':False})
        
        for link in chapters_links:
            chapter_name = link.find('span', class_=r'\"chapter-text\"').get_text()
            
            # Chapter_name_response = Chapter 77<\/span>\n.......
            chapter_name = chapter_name.split('<')[0]

            # Chapter_link from html = \"https:\/\/animedaily.net\/absolute-resonance-novel\/chapter-80.html\"
            chapter_link = (link['href']).split('"')[1]
            chapter_link = re.sub(r"\\/", '/',chapter_link)[:-1]
            
            pattern = r'(.*) (\d+)'
            match = re.match(pattern,chapter_name)
            chapter_num = int(match.group(2))

            if self.ending_number is not None:
                if chapter_num in NovelScraper.inclusive_range(self.starting_number, self.ending_number):
                    self.chapter_url_dict[chapter_name] = chapter_link
                if chapter_num==self.ending_number:
                    raise ChapterListExhausted
            else:
                self.chapter_url_dict[chapter_name] = chapter_link

        pass

    def create_md(self):
        super().create_md()

        for chapter_name, link in self.chapter_url_dict.items():
            self._get_html_response(url=link)
            self.chapter_name = chapter_name
            self.content = self.soup.find_all('p')[:-3]
            self._write_doc()


class NovelBin(NovelScraper):
    def __init__(self, url, 
                 selected_option: str = None, 
                 starting_number: int = 1, 
                 ending_number: int = None, 
                 output_format: str = None, 
                 headers=None):
        super().__init__(url, selected_option, starting_number, ending_number, output_format, headers)
        self.novel_id: str = None

    def get_novel_details(self):
        super().get_novel_details()

        self.novel_name = self.soup.find('h3', class_ = "title").get_text()
        self.author = (self.soup.find('h3', string= 'Author:')).find_next_sibling('a').text.strip()
        print(self.novel_name, self.author)




novel_full_url: str = "https://novelfull.com/absolute-resonance.html"
anime_daily_url: str = "https://animedaily.net/absolute-resonance-novel.html"
novel_bin_url: str = "https://novelbin.com/b/coiling-dragon"

absolute_res_nf = NovelFull(novel_full_url, starting_number=34, ending_number=60)
# x = absolute_res_nf.get_chapter_list()
# print(x)

absolute_res_ad = AnimeDaily(anime_daily_url,ending_number=60)

# x = absolute_res_ad.get_novel_details()
# print(x)
# print(absolute_res_ad.starting_number)
# absolute_res_ad.get_final()

coiling_drag_nb = NovelBin(novel_bin_url)
coiling_drag_nb.get_novel_details()