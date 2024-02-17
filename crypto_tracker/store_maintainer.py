import os, csv
import datetime as dt

max_val_store_day = 7
time_now = dt.datetime.now()

def main():
    wd = os.getcwd()
    path = os.path.join(wd+"\\Stores")
    os.chdir(path)

    file_list = os.listdir()

    for index, file in enumerate(file_list, start=1):
        with open(f'{file}') as crypto_log:
            next(crypto_log)
            if index == 1:
                for line in crypto_log:
                    row_value = (line.strip()).split(',')
                    date_time = dt.datetime.strptime(row_value[-1],"%Y %m %d - %I:%M:%S %p")

                    delta_time = time_now-date_time
                    # print(delta_time.seconds/(60*60))

                    if delta_time.days > 7:
                        del line


def error_logger(error, msg):
    # try:
    #     with open('Error_logger.txt', 'a', newline='') as log:
    #         log.write(f'{error.__name__} occurred at {time_now} - {str(error)}')
    # except FileNotFoundError:
    #     with open('Error_logger.txt', 'w', newline='') as log:
    #         log.write(f'{error.__name__} occurred at {time_now} - {str(error)}')

    print(f'{error.__name__} occurred at {time_now} - {msg}')
    # print(error)

if __name__ == '__main__':
    main()

    a = '2'
    b = 3
    try:
        print(a+b)
    except TypeError as e:
        error_logger(TypeError, e)

    # e = raise ConnectionError
    # error_logger(raise ConnectionError)