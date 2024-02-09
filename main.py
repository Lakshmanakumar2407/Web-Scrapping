import time, schedule
import Coinmarket_scrape as cs
import coinmarket_write as cw

def main():
    cs.main()
    time.sleep(2)
    cw.main()

if __name__ == "__main__":
    # schedule.every(1).minutes.do(main)
    # while True:
    #     schedule.run_pending()  
    while True:
        main()
        time.sleep(60)