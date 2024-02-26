1. List the website to scrpae for novel
   1. ~~Novelfull.com~~
   2. ~~Animedaily.net~~
   3. ~~Novelbin.com~~
   4. Box-novel.com
   5. Freewebnovel.com
2. ~~Try 2 or 3 website first and identify the commonly used methods~~
3. Try implementing OOP concepts since its the primary focus of this exercise
4. ~~Write Docstrings - **Used GPT Help**~~
5. ~~Add the option to download by book or volume or chapter (now it's only chapter) and change the default value of starting chap num to 1~~

Issues

1. Chapter start ok ending none issue - **Resolved**
   1. One limitation of the code is that , If i want to start scrapin from chapter 20, till end without mentioning the ending number, It will throw error. because ending_number_by default is set to none.
   2. If i Want to include this functionality I need to load the entire chapter list into memory, which will more reuqests, to websites which lists chapter by page. I don't want that so I limited by it
   3. is there a way to solve both, without loading entire chapters?????
   4. May be if I set ending nhumber to be a extremely large number by default??
   5. Worked !!!!
2. Rate limit issue?? - **WILL DO AFTER LEARNIGN ASYNCIO**
   1. Some website have rate limits beyond which i can't send request. And it's also ethically wrong to overload their websie
   2. If I introduce rest time after each request then for lot of chapters the overall runtime will be huge...
   3. One possible idea, I could think of is...
      1. get just novel, optinal start_num, optional end_num
      2. search for novel is multiple available website using reuqests module and structure url according to novel routes.
      3. If response is successfull then select those websites alone.
      4. Check if the no of chapters are same in all websites.
      5. Need to figure out the remaining logic.... possibly send requests using async module. 

