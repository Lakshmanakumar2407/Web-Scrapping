import random, re, subprocess, time
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

    default_start_number = 1
    extremely_large_number = 1000000000000000

    def __init__(self, url,
                 starting_number: int = None, 
                 ending_number: int =None, 
                 output_format: str = None,
                 headers=None) :
        '''
        This is a constructor method for the baseclass
        Contains some of the required attributes some which are passed by the user otherwise, initialised for internal usage
        '''
        self.site_url: str = url
        self.starting_number: int = starting_number
        self.ending_number: int = ending_number
        self.output_format: str = output_format
        self.headers: dict = headers or {'User-Agent':random.choice(NovelScraper.list_of_ua)}
        self.session = None
        self.params: dict = None
        self.payload: dict = None
        self.soup = None
        self.chapter_url_dict: dict = None

    def _create_session(self):
        self.session = requests.session()
        return self.session
    
    def _get_html_response(self, method = 'GET', url: str = None):
        try:
            if self.session is None:
                self._create_session()

            url = url or self.site_url
            response = self.session.request(method, 
                                            url, 
                                            headers=self.headers, 
                                            params=self.params,
                                            data= self.payload, 
                                            timeout=10)
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

    def chapter_renamer(self):
        if ":" in self.novel_name:
            self.novel_name = self.novel_name.replace(':','-')

    def _touch_doc(self):
        self. chapter_renamer()

        with open(f"{self.novel_name}.md",'w', encoding="utf-8") as novel:
            novel.write(f'# {self.novel_name} \n\n')
            novel.write(f'*{self.author}* \n\n')
        
        self.chapter_name: str = None
        self.content: list = None

        return None
    
    def create_md(self):
        self.get_novel_details()
        self.get_chapter_list()
        self._touch_doc()

    def _write_doc(self):
        with open(f'{self.novel_name}.md','a', encoding="utf-8") as novel:
            novel.write(f'## {self.chapter_name}\n\n')
            for content in self.content:
                novel.write('\n')
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
                 starting_number: int= NovelScraper.default_start_number, 
                 ending_number: int = NovelScraper.extremely_large_number, 
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

        self._get_html_response()

        pattern = r'(\w*)\s(\d+)'
        chpter = (self.soup.find('div', attrs={"class":"col-xs-12", "id":"list-chapter"})).find_all('a', attrs={'href':True, 'title':True})
        
        for chp in chpter:
            match = re.search(pattern, chp.text)
            chapter_num = int(match.group(2))
            chapter_name = chp.get_text()
            chapter_link = self.base_url+chp['href']

            if self.starting_number != NovelScraper.default_start_number or \
                self.ending_number != NovelScraper.extremely_large_number:

                if self.starting_number <= chapter_num <= self.ending_number:
                    self.chapter_url_dict[chapter_name] = chapter_link

                if chapter_num > self.ending_number:
                    raise ChapterListExhausted
            else:
                self.chapter_url_dict[chapter_name] = chapter_link

    def create_md(self):
        super().create_md()

        for chp_name, link in self.chapter_url_dict.items():
            self.site_url = link
            self.soup = self._get_html_response()
            self.chapter_name = chp_name
            self.content = self.soup.find_all('p')[3:-1]
            self._write_doc()
            time.sleep(2)


class AnimeDaily(NovelScraper):
    def __init__(self, url, 
                 starting_number: int=NovelScraper.default_start_number, 
                 ending_number: int= NovelScraper.extremely_large_number, 
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
                self._fetch_chapter_url_from_page()
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
            
            # pattern = r'(\w*)\s(\d+)'
            pattern = r'([^0-9]*)\s0*(\d+)\b'
            match = re.match(pattern,chapter_name)
            chapter_num = int(match.group(2))

            if self.starting_number != NovelScraper.default_start_number or \
                self.ending_number != NovelScraper.extremely_large_number:

                if self.starting_number <= chapter_num <= self.ending_number:
                    self.chapter_url_dict[chapter_name] = chapter_link

                if chapter_num > self.ending_number:
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
            print(f'Finsihed writing - {self.chapter_name}')


class NovelBin(NovelScraper):
    def __init__(self, url,  
                 starting_number: int = NovelScraper.default_start_number, 
                 ending_number: int = NovelScraper.extremely_large_number, 
                 output_format: str = None, 
                 headers=None):
        super().__init__(url, starting_number, ending_number, output_format, headers)
        self.novel_id: str = None
        self.secret_url = "https://novelbin.com/ajax/chapter-archive"

    def get_novel_details(self):
        super().get_novel_details()

        self.novel_name = self.soup.find('h3', class_ = "title").get_text()
        self.author = (self.soup.find('h3', string= 'Author:')).find_next_sibling('a').text.strip()
        
        return self.novel_name, self.author

    def _get_novel_id(self):
        pattern = r'/b/(\w+(?:-\w+)*)'
        match = re.search(pattern, self.site_url)
        self.novel_id = match.group(1)

        return self.novel_id
    
    def _get_secret_page(self):
        self._get_novel_id()

        s_url = self.secret_url
        self.params = {
            'novelId':self.novel_id
        }
        self._get_html_response(url=s_url)
        
        return None

    def get_chapter_list(self):
        self._get_secret_page()
        self.chapter_url_dict = dict()

        chapters = self.soup.find_all('a', attrs={'href':True, 'title':True})
        for chp in chapters:
            chapter_name = chp['title']
            chapter_link = chp['href']

            if  self.starting_number != NovelScraper.default_start_number or \
                self.ending_number != NovelScraper.extremely_large_number:

                pattern = r'([^0-9]*)\s*0*(\d+)\b'
                # pattern = r'\b\s*(?:Chapter|Book|Volume|:)\s*0*(\d+)\b'
                match = re.match(pattern, chapter_name)
                chapter_num = int((match.group(2)))
                # print(chapter_num, chapter_name)

                if self.starting_number <= chapter_num <= self.ending_number:
                    self.chapter_url_dict[chapter_name] = chapter_link

                if chapter_num > self.ending_number:
                    # print('breakng')
                    break
            else:
                self.chapter_url_dict[chp['title']] = chp['href']

        return self.chapter_url_dict

    def create_md(self):
        super().create_md()

        for chapter_name, chapter_link in self.chapter_url_dict.items():
            self.chapter_name = chapter_name
            self._get_html_response(url=chapter_link)
            time.sleep(2)
            self.content = self.soup.find_all('p')[1:]
            self._write_doc()
            print(f'Wrote chapter - {chapter_name}')


class FreeWebNovel(NovelScraper):
    def __init__(self, 
                 url, 
                 starting_number: int = NovelScraper.default_start_number, 
                 ending_number: int = NovelScraper.extremely_large_number, 
                 output_format: str = None, 
                 headers=None):
        super().__init__(url, starting_number, ending_number, output_format, headers)
        self.base_url: str = "https://freewebnovel.com" 
        self.chapter_url: str = None

    def get_novel_details(self):
        super().get_novel_details()

        self.novel_name = self.soup.find('h3', class_ = "tit").get_text()
        self.author = self.soup.find('a', class_ = 'a1', attrs={'href':True, 'title':True}).get_text()

        return self.novel_name, self.author
    
    def get_chapter_list(self):
        self.get_novel_details()
        self.chapter_url_dict = dict()

        chapter_list = (self.soup.find('div', class_ = "m-newest2")).find_all('a', class_ = "con", attrs={"href":True, "title":True})

        for chapter in chapter_list:
            chapter_name: str = chapter.get_text()
            self.chapter_url = self.base_url + chapter['href']

            if self.starting_number != NovelScraper.default_start_number or \
                self.ending_number != NovelScraper.extremely_large_number:
                
                pattern = r'([^0-9]*)\s*0*(\d+)\b'
                match = re.match(pattern, chapter_name)
                chapter_num: int = int(match.group(2))

                if self.starting_number <= chapter_num <= self.ending_number:
                    self.chapter_url_dict[chapter_name] = self.chapter_url

                if chapter_num > self.ending_number:
                    break

            else:
                self.chapter_url_dict[chapter_name] = self.chapter_url

        return self.chapter_url_dict

    def create_md(self):
        super().create_md()

        for chapter_name, chapter_link in self.chapter_url_dict.items():
            self.chapter_name = chapter_name
            self._get_html_response(url=chapter_link)
            self.content = self.soup.find_all('p')[1:-1]
            self._write_doc()
            print(f'Finished Writing chapter - {chapter_name}')
            

class BoxNovel(NovelScraper):
    def __init__(self, 
                 url, 
                 starting_number: int = NovelScraper.default_start_number, 
                 ending_number: int = NovelScraper.extremely_large_number, 
                 output_format: str = None, 
                 headers=None):
        super().__init__(url, starting_number, ending_number, output_format, headers)
        self.chapter_url: str = ""

    def get_novel_details(self):
        super().get_novel_details()

        self.novel_name = self.soup.find('div', class_ = "post-title").find('h1').get_text().strip()
        self.author = self.soup.find('div', class_ = "author-content").get_text().strip()

        return self.novel_name, self.author

    def get_chapter_list(self):
        self.get_novel_details()
        self.chapter_url_dict = dict()
        url_to_pass = self.site_url+'ajax/'+'chapters'

        self._get_html_response(method='POST', url=url_to_pass)
        chapters = self.soup.find_all('a', attrs={'href':True, 'title':False})
        chapters.reverse() # in  this webpage, Latest is structued first
        
        for chapter in chapters:
            chapter_name = chapter.get_text().strip()
            chapter_link = chapter['href']

            if self.starting_number != NovelScraper.default_start_number or \
                self.ending_number != NovelScraper.extremely_large_number:

                pattern = r'([^0-9]*)\s*0*(\d+)\b'
                match = re.match(pattern, chapter_name)
                chapter_num: int = int(match.group(2))

                if self.starting_number <= chapter_num <= self.ending_number:
                    self.chapter_url_dict[chapter_name] = chapter_link

                if chapter_num > self.ending_number:
                    break

        return self.chapter_url_dict

    def create_md(self):
        super().create_md()

        for chapter, link in self.chapter_url_dict.items():
            self.chapter_name = chapter
            self._get_html_response(url=link)
            self.content = self.soup.find('div', class_ = 'text-left').find_all('p')[1:]
            self._write_doc()
            print(f'Finsihed writing - {self.chapter_name}')




novel_full_url: str = "https://novelfull.com/battle-through-the-heavens.html"
anime_daily_url: str = "https://animedaily.net/absolute-resonance-novel.html"
novel_bin_url: str = "https://novelbin.com/b/battle-through-the-heavens-novel"
free_web_novel_url : str = "https://freewebnovel.com/divine-throne-of-primordial-blood.html"
box_novel_url: str = "https://boxnovel.com/novel/top-tier-providence-secretly-cultivate-for-a-thousand-years/"


btth_nf = NovelFull(novel_full_url, output_format='epub')
# print(absolute_res_nf.ending_number, absolute_res_nf.starting_number)
# x = absolute_res_nf.get_chapter_list()
btth_nf.get_final()

absolute_res_ad = AnimeDaily(anime_daily_url,starting_number=18, ending_number=30, output_format='epub')
# x = absolute_res_ad.get_chapter_list()
# absolute_res_ad.get_final()

btth_nb = NovelBin(novel_bin_url, 'epub')
# x = coiling_drag_nb.get_chapter_list()
# print(x)
btth_nb.get_final()

free_web_novel_n = FreeWebNovel(free_web_novel_url, ending_number=1, output_format='epub')
# free_web_novel_n.get_final()

box_novel_n = BoxNovel(box_novel_url, 1, 10,'pdf')
# box_novel_n.create_md()
# box_novel_n.get_final()
# x = box_novel_n.get_novel_details()
print(box_novel_n)
# box_novel_n._touch_doc()