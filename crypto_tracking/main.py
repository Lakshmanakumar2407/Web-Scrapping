import time, os
import datetime as dt
import coinmarket_scrape as cs
import coinmarket_write as cw
import store_analyse as sa
import store_maintainer as sm
import common_utilities as cu
import config

def main():
    # file_path = "C:\\Users\\laksh\\Documents\\Repos\\web_scrapping_Stuff"
    current_directory = os.getcwd()

    working_directory = os.path.join(current_directory, 'crypto_tracking')

    os.chdir(working_directory)
    # print(os.getcwd())

    cs.fetch()

    cw.record_data(config.fields_to_record)

    # Lazy loading
    cryptos_to_track = config.files_to_track()
    sa.analyse_filter(cryptos_to_track, config.user_tracking_dict)

    sm.store_cleaner(config.max_time_to_store)

    cu.activity_logger('------------------')

    os.chdir(current_directory)
    # print(os.getcwd())
    print(f'Last executed on {dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}')



if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)