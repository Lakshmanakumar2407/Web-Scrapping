import os


fields_to_record = ['cmcRank','price','circulatingSupply','volume24h']

def files_to_track():
    # File list to Track
    present_directory = os.getcwd()
    to_directory = os.path.join(present_directory,'stores')
    os.chdir(to_directory)

    cryptos_to_track = [file.split('.')[0] for file in os.listdir()]
    # print(cryptos_to_track)

    os.chdir(present_directory)

    return cryptos_to_track

user_tracking_dict = {'price':[1, 10], 'volume24':[1.0, 10]}

max_time_to_store = 1