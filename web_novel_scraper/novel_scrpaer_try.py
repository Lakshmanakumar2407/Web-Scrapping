from novel_scraper import NovelScraper

site_url: str = "https://novelfull.com/absolute-resonance.html"
s_u = "https://novelfull.com"

scraper1 = NovelScraper(site_url)
scraper2 = NovelScraper(s_u)

print(scraper1.__dict__,'\n\n', scraper2.__dict__,'\n\n', NovelScraper.__dict__
      , '\n\n', scraper1.headers,'\n\n', scraper2.headers)