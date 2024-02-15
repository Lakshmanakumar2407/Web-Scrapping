'''
Lesson Learnt: First know what you need and what the output should be before even touching keyboard.
Now I need to redo this
'''

import os
import datetime as dt

def start_here():
    store_path = os.path.join(os.getcwd(),'Stores')
    os.chdir(store_path)
    print(os.getcwd())
    file_list = os.listdir()

    dict_with_datetime_as_key = dict()

    with open('Bitcoin.csv') as crypto_file:

        cmcRank_list, circulatingSupply_list, price_list, volume24_list, datetime_list = [], [], [], [], []
        next(crypto_file)

        for line in crypto_file:

            row_values = (line.strip()).split(',')
            _cmcRank, _circulatingSupply, _price, _volume24, _datetime_str = row_values

            dict_with_datetime_as_key.update(
                {dt.datetime.strptime(_datetime_str,"%Y %m %d - %I:%M:%S %p"):[_cmcRank,_circulatingSupply,_price,_volume24]})
            
            # print(dict_with_datetime_as_key)
                  
        user_required_datetime = time_filter(dict_with_datetime_as_key,20)
        # print(user_required_datetime)

        user_required_delta_lod = val_track(dict_with_datetime_as_key, user_required_datetime, 'price', 'volume24')
        # print(len(user_required_delta_lol),user_required_delta_lol)

        trigger_email(user_required_delta_lod, [0.2, 1])
    

def time_filter(some_dict, time_interval_in_minutes):
    
    time_val = [time for time in some_dict]
    time_interval_in_seconds = time_interval_in_minutes*60
    time_diff = 0

    filtered_time = list()
    filtered_time.append(time_val[0])

    for i in range(1, len(time_val)):
        time_diff += (time_val[i] - time_val[i-1]).seconds
        if time_diff >= time_interval_in_seconds:
            filtered_time.append(time_val[i])
            # print(time_diff, time_interval_in_seconds)
            time_diff = 0
    
    return filtered_time

def val_track(some_dict, required_datetime, *args):

    default_mapper = {
        'cmcRank':0, 
        'circulatingSupply':1,
        'price':2,
        'volume24':3
            }

    user_mapper = {tag:value for tag,value in default_mapper.items() if tag in args}
    # print(user_mapper)

    user_required_data_values = [vals for times,vals in some_dict.items() if times in required_datetime]
    user_required_data_keys = [times for times,vals in some_dict.items() if times in required_datetime]

    percent_diff_lod = list()

    len_user_req_data, len_of_val = len(user_required_data_values),len(user_required_data_values[0])

    for i in range(1,len_user_req_data):
        temp_list, temp_dict = list(), dict()
        for k in range(len_of_val):
            if k in user_mapper.values():
                new_data = round(float(user_required_data_values[i][k]),5)
                old_data = round(float(user_required_data_values[i-1][k]),5)
                temp_list.append(((new_data-old_data)/old_data)*100)
                # print(old_data,new_data,temp_dict)
            temp_dict[user_required_data_keys[i]] = temp_list
        percent_diff_lod.append(temp_dict)
        # print(percent_diff_lod)
    
    return percent_diff_lod

def trigger_email(some_list_of_dict, *args):

    params = [val for arg in args for val in arg]

    for every_dict in some_list_of_dict:
        for date_time, values in every_dict.items():
            for index, i_values in enumerate(values):
                if i_values>params[index]:
                    print(i_values, index, date_time)


if __name__ == "__main__":
    start_here()