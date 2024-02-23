import os

max_retries = 5

fields_to_record = ['cmcRank','price','circulatingSupply','volume24h']

def files_to_track():
    # File list to Track
    present_directory = os.getcwd()
    to_directory = os.path.join(present_directory,'stores')
    os.chdir(to_directory)

    cryptos_to_track = [file[:-4] for file in os.listdir()]
    # print(cryptos_to_track)

    os.chdir(present_directory)

    return cryptos_to_track

user_tracking_dict = {'price':[3, 10], 'volume24':[3.0, 20]}

max_time_to_store = 5




email_address = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASS')
smtp_server = 'smtp.gmail.com'
smtp_port = 465