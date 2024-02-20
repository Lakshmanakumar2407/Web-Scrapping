import datetime as dt
import os
import smtplib
import config


# print(os.getcwd())

def error_logger(error, msg):
    """
    This function is meant for logging when error occured - It is imported into other working file to log

    1. When called It will write the error, time it occured an error message in error.txt
    """

    time_at_calling = dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    try:
        with open('error_logger.txt', 'a', newline='') as log:
            log.write(f'{error.__name__} occurred at {time_at_calling} - {msg}\n')
    except FileNotFoundError:
        with open('error_logger.txt', 'w', newline='') as log:
            log.write(f'{error.__name__} occurred at {time_at_calling} - {msg}\n')


def send_email(message, *args):

    with smtplib.SMTP_SSL(config.smtp_server, config.smtp_port) as emailer:
        emailer.login(config.email_address, config.password)
        emailer.sendmail(config.email_address, config.email_address, message)


def activity_logger(message):
    time_at_calling = dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    try:
        with open('activity_logger.txt', 'a', newline='') as log:
            log.write(f'{message} - performed on {time_at_calling}\n')
    except FileNotFoundError:
        with open('activity_logger.txt', 'w', newline='') as log:
            log.write(f'{message} - performed on {time_at_calling}\n')