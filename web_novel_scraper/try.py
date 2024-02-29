import novel_scraper as scraper

url = "https://boxnovel.com/novel/top-tier-providence-secretly-cultivate-for-a-thousand-years/"

# inst = scraper.BoxNovel(url, 20, 40, 'epub')
# x = inst.get_novel_details()
# print(x)
# y = inst.get_chapter_list()
# for a,b ,in y.items():
#     print(a,'  -  ',b)
# inst.get_final()

scraper.BoxNovel(url,20,40).get_final()