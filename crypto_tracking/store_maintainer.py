import os, csv
import datetime as dt
import common_utilities as cu

max_val_store_day = 3600

def store_cleaner(max_time_val):
    cu.activity_logger("Cleaning old data....")

    # print('Entered Store cleaner')
    wd = os.getcwd()
    # print(wd)
    path = os.path.join(wd+"\\Stores")
    # print(path)
    os.chdir(path)

    file_list = os.listdir()

    for file in file_list:
        filtered_data = collect_only_required_rows(file, max_time_val)
        # print(filtered_data)
        with open(f'{file}_temp.csv', 'w') as new_write:
            new_write.writelines(filtered_data)
        os.remove(f'{file}')
        os.rename(f'{file}_temp.csv', f'{file}')
    
    os.chdir(wd)
    # print(os.getcwd())

def collect_only_required_rows(file, max_time):
    temp_val_holder = []

    with open(f'{file}') as crypto_log:
        temp_val_holder.append(next(crypto_log))

        for line in crypto_log:
            row_value = (line.strip()).split(',')
            delta_time = delta_time_calc(row_value[-1])
            # print(delta_time.seconds)

            if delta_time.days < max_time:
                temp_val_holder.append(line)
    
    return temp_val_holder

def delta_time_calc(date_time_str):
    date_time_at_call = dt.datetime.now()
    date_time_given = dt.datetime.strptime(date_time_str,"%Y %m %d - %I:%M:%S %p")

    delta_time = date_time_at_call - date_time_given
    return delta_time

if __name__ == '__main__':
    store_cleaner(max_val_store_day)