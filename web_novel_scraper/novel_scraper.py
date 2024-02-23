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
                 starting_chapter=None, 
                 ending_chapter=None, 
                 output_format = None,
                 headers=None) :
        
        self.site_url: str = url
        self.starting_chapter: int = starting_chapter
        self.ending_chapter: int = ending_chapter
        self.output_format: str = output_format
        if headers is None:
            self.headers: dict = {
                'User-Agent':random.choice(NovelScraper.list_of_ua)
            }
        else:
            self.headers = headers
        self.session = None
        self.soup = None
        self.novel_name: str = None
        self.author = None
        self.chapter_name = None
        self.content = None

    def _create_session(self):
        self.session = requests.session()
        return self.session
    
    def _get_html(self):
        try:
            if self.session is None:
                self._create_session()
            response = self.session.get(self.site_url, headers=self.headers, timeout=10)
            response.raise_for_status()
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
                self.soup = BeautifulSoup(response.text, 'lxml')
                return self.soup
            else:
                print(f'Bad response : {response.status_code}')
                return None
            
    def _touch_doc(self):
        with open(f'{self.novel_name}.md','w', encoding="utf-8") as novel:
            novel.write(f'# {self.novel_name} \n\n')
            novel.write(f'*{self.author}* \n\n')
        
        return None
    
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
            # subprocess.check_output(pandoc_command)
            subprocess.run(pandoc_command, check= True)
            print("Your File is ready")
        except subprocess.CalledProcessError as e:
            print(f'Error - {e}')

    @staticmethod
    def inclusive_range(start, stop):
        return range(start, stop+1)
    
class ChapterListExhausted(Exception):
    pass

class NovelFull(NovelScraper):
    def __init__(self, url: str, 
                 starting_chapter: int= None, 
                 ending_chapter: int = None, 
                 output_format: str = None, 
                 header: dict = None):
        super().__init__(url, starting_chapter, ending_chapter, output_format, header)
        self.last_page_num = None
        self.base_url = r'https://novelfull.com'
        self.page_search_url = None
        self.chapter_url_dict = dict()

    def get_novel_details(self) -> tuple[str, str]:
        self._get_html()
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

        print("getting pages...")

        for counter in range(self.last_page_num):
            print(f"Adding Chapters...... {counter}")
            self.site_url = self.base_url+self.page_search_url+str(counter+1)
            try:
                self._fetch_chapter_url_from_page()
            except ChapterListExhausted:
                break
        
        return self.chapter_url_dict

    def _fetch_chapter_url_from_page(self): 
        self.soup = self._get_html()

        pattern = r'Chapter (\d+)'
        chpter = (self.soup.find('div', attrs={"class":"col-xs-12", "id":"list-chapter"})).find_all('a', attrs={'href':True, 'title':True})
        
        for chp in chpter:
            match = re.search(pattern, chp.text)
            chapter_num = int(match.group(1))
            if self.starting_chapter and self.ending_chapter is not None:
                if chapter_num in NovelScraper.inclusive_range(self.starting_chapter, self.ending_chapter):
                    self.chapter_url_dict[chp.get_text()] = self.base_url+chp['href']
                if chapter_num == self.ending_chapter:
                    raise ChapterListExhausted
            else:
                self.chapter_url_dict[chp.get_text()] = self.base_url+chp['href']

    def create_md(self):
        self.get_chapter_list()
        self._touch_doc()

        for chp_name, link in self.chapter_url_dict.items():
            self.site_url = link
            self.soup = self._get_html()
            self.chapter_name = chp_name
            self.content = self.soup.find_all('p')[3:-1]
            self._write_doc()

    def get_final(self):
        self.create_md()
        self._convert_md()

class AnimeDaily(NovelScraper):
    def __init__(self, url, 
                 starting_chapter=None, 
                 ending_chapter=None, 
                 output_format=None, 
                 headers=None):
        super().__init__(url, starting_chapter, ending_chapter, output_format, headers)

    
site_url: str = "https://novelfull.com/absolute-resonance.html"

absolute_res = NovelFull(site_url,1,10,'epub')
absolute_res.n