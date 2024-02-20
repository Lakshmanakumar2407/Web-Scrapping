import os, csv, pytz
import datetime as dt 
import common_utilities as cu

# UNCOMMENT THE BELOW CODE ONLY WHEN YOU ARE RUNNING THIS FILE DIRECTLY AND THE CODE AT IF BLOCK BELOW
# wd = os.getcwd()
# # print(wd)
# os.chdir(wd+'/crypto_tracking')

def record_data(fields_to_record):
    # print('Entered coinmarket write')
    global fetched_date_time_raw

    cu.activity_logger('Recording Data')

    try: 
        with open('index.csv') as index:
            first_line = next(index)
            row_val = (first_line).split(' : ')
            fetched_date_time_raw = dt.datetime.strptime((row_val[-1]).strip(),"%B %d, %Y | %I:%M:%S %p")
            # print(fetched_date_time_raw)
            index_reader = csv.DictReader(index)

            current_directory = os.getcwd()
            # print(current_directory)
            to_directory = os.path.join(current_directory, 'stores')
            os.chdir(to_directory)
            write_data(index_reader, fields_to_record)
            os.chdir(current_directory)
            # print(os.getcwd())

    except FileNotFoundError :
        print('File not Found, error in module {__name__}')

def write_data(dictreader_obj, choosen_field_list):
    local_time = pytz.timezone('Asia/Kolkata')

    for index, diction in enumerate(dictreader_obj, start=1):
        file_name = diction.get('name')
        temp_diction = {tag:value for tag,value in diction.items() if tag in choosen_field_list}
        temp_diction.update({'fetched_on':fetched_date_time_raw.strftime("%Y %m %d - %I:%M:%S %p")})
        field_head = list(temp_diction.keys())
        
        if not os.path.isfile(f'{file_name}.csv') or os.path.getsize(f'{file_name}.csv') == 0:
            with open(f'{file_name}.csv','w',newline='') as writer:
                writer_csv = csv.DictWriter(writer,fieldnames=field_head)
                writer_csv.writeheader()
        with open(f'{file_name}.csv','a',newline='') as writer:
                writer_csv = csv.DictWriter(writer,fieldnames=field_head)
                writer_csv.writerow(temp_diction)

if __name__ == '__main__':
    choosen_field = ['cmcRank','price','circulatingSupply','volume24h']
    record_data(choosen_field)