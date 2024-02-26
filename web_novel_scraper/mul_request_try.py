import novel_scraper as scrapper
import asyncio, time

# WILL DO THIS AFTER LEARNIGN ASYNCIO

novel_full_url: str = "https://novelfull.com/absolute-resonance.html"
anime_daily_url: str = "https://animedaily.net/absolute-resonance-novel.html"
novel_bin_url: str = "https://novelbin.com/b/absolute-resonance"

x, y, z = None, None, None
first = 1
last = 100

async def nf():
    nf = scrapper.NovelFull(novel_full_url, first, last)
    result = nf.get_chapter_list()
    return result

async def ad():
    ad = scrapper.AnimeDaily(anime_daily_url, first, last)
    result = ad.get_chapter_list()
    return result

async def nb():
    nb = scrapper.NovelBin(novel_bin_url, first, last)
    result = nb.get_chapter_list()
    return result

async def main():
    global x, y, z
    tasks = [nf(), ad(), nb()]

    for coro in asyncio.as_completed(tasks):
        result = await coro
        if coro == tasks[0]:
            x = result
        elif coro == tasks[1]:
            y = result
        elif coro == tasks[2]:
            z = result

# Measure time taken for asyncio approach
st = time.time()
asyncio.run(main())
et = time.time()
dt_asyncio = et - st

print(f"Asyncio result: , Time: {dt_asyncio}")


def normal():
    global x,y,z
    nf = scrapper.NovelFull(novel_full_url, first, last)
    x =  nf.get_chapter_list()
    nb = scrapper.NovelBin(novel_bin_url, first, last)
    y =  nb.get_chapter_list()
    nb = scrapper.NovelBin(novel_bin_url, first, last)
    z = nb.get_chapter_list()

# Measure time taken for synchronous approach
st = time.time()
normal()
et = time.time()
dt_normal = et - st

print(f"Synchronous result: {len(x)}, {len(y)}, {len(z)}, Time: {dt_normal}")