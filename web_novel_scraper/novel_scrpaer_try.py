import novel_scraper as ns

site_url: str = "https://novelfull.com/absolute-resonance.html"

absolute_res = ns.NovelFull(site_url)
absolute_res.write_doc()
# absolute_res.get_html()
# novel_name, author_name = absolute_res.get_novel_details()
# absolute_res.get_pages()
# print(absolute_res.novel_name, absolute_res.author,absolute_res.last_page_num, absolute_res.page_search_url)
# absolute_res.get_chapter_list()

# # for chapter, link in absolute_res.chapter_url_dict.items():
# #     print(chapter,' - ', link)

# # print(absolute_res.site_url)
# absolute_res.write_doc()
