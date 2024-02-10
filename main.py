import time, schedule ,random
import Coinmarket_scrape as cs
import coinmarket_write as cw

def main():
    cs.main()
    time.sleep(1)
    cw.main()

if __name__ == "__main__":
    # schedule.every(1).minutes.do(main)
    # while True:
    #     schedule.run_pending()  
    while True:
        main()
        time.sleep(random.randint(250,300))