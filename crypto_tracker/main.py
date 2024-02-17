import time, os, schedule ,random
import datetime as dt
import coinmarket_scrape as cs
import coinmarket_write as cw
import store_analyse as sa

def main():
    cs.main()
    time.sleep(1)
    cw.main()
    time.sleep(1)

    wd = os.getcwd()
    os.chdir(wd+'\\Stores')
    user_crypto_list1 = os.listdir()
    os.chdir(wd)
    user_tracking_dict = {'price':[1, 10], 'volume24':[1, 10]}
    sa.start_here(user_crypto_list1,user_tracking_dict)
    print(f'completed last run on {dt.datetime.now()}')

if __name__ == "__main__":
    # schedule.every(1).minutes.do(main)
    # while True:
    #     schedule.run_pending()  
    while True:
        main()
        time.sleep(300)