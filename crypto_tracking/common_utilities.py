import datetime as dt
import os
import smtplib

# print(os.getcwd())

def error_logger(error, msg):
    """
    This function is meant for logging when error occured - It is imported into other working file to log

    1. When called It will write the error, time it occured an error message in error.txt
    """

    time_at_calling = dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    try:
        with open('er_logger.txt', 'a', newline='') as log:
            log.write(f'{error.__name__} occurred at {time_at_calling} - {msg}')
    except FileNotFoundError:
        with open('er_logger.txt', 'w', newline='') as log:
            log.write(f'{error.__name__} occurred at {time_at_calling} - {msg}')

    print("Error logged - check for detailed info at er_logger.txt")
