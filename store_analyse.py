'''
Lesson Learnt: First know what you need and what the output should be before even touching keyboard.
Now I need to redo this

INPUTS FROM USER

1. List of crypto's to track from top 100 
2. dict of Column fields as keys and by what percent in float and time interval(minutes) as list as value to key. 
    IF increasing +ve, decreasing -ve
    2.1 Future work - Calculate both sides up or down
OUTPUT

1. Send a combined text message as email if the crypto's prametrs in list exceeds the user specifiec percent
'''

import os
from collections import OrderedDict
import datetime as dt

# List of Crypto's to track
user_crypto_list = ['Bitcoin', 'Aave', 'Beam', 'Cardano']
# user_crypto_list = ['Bitcoin']

# Parameters as key : percent and time interval as key
user_tracking_dict = {'price':[0.1, 10], 'volume24':[1.0, 10]}

# fields available in the stored csv
default_mapper = {
        'cmcRank':0, 
        'circulatingSupply':1,
        'price':2,
        'volume24':3
            }

def start_here(list_of_crypto_to_track, dict_with_params):
    '''
    Rough logic before starting to code

    So what i need to get from stores is time sereis of data 
    Task 1 ✔
    -> dict with single params and corresponing time intervaled value 
            (Like if the user want the time interval to be 10 minutes for price parameter
                then the dict would be like
                {
                    datetime_object:value_at_that_datetime
                    datetime_object + delta_time: value_at_that_datetime
                    ....
                    ..
                }
             like this for each parameter specified by the user) 
    
    Task 2 
    -> Pass the time_interval filtered data to percent check function
    -> The function should return dict of dict for only the value which pass the user percent
    '''

    store_path = os.path.join(os.getcwd(),'Stores')
    os.chdir(store_path)

    # filter only the user required params from deault mapper
    paramsdict_wih_index = {key:dict_with_params[key] + [value] 
                            for key,value in default_mapper.items() 
                            if key in dict_with_params}

    # Dict which will contain info all the changes as per the user criteria
    master_dict = dict()

    for crypto in list_of_crypto_to_track:
        filtered_time_dod = filter_data_user(crypto, paramsdict_wih_index)
        filtered_percent_dod = user_percent_filter(filtered_time_dod, paramsdict_wih_index)

        if filtered_percent_dod != {}:
            master_dict[crypto] = filtered_percent_dod

    dict_with_latest_values = latest_value_filter(master_dict)
    # print(dict_with_latest_values)

    for crypto in dict_with_latest_values:
        if len(dict_with_latest_values[crypto]) != 0:
            string_construct(crypto, dict_with_latest_values[crypto])
       
def filter_data_user(file_name, dict_with_user_params_and_vals ):
    '''Dicts values lists first value is percent_inrease, time_interval_minutes, index_of_the_param 
    
    I need to return a dict of dict with dict key being the parameter and value being the time series data
    '''

    params_timeseries_dict_of_dicts = dict()

    # for loop will be used here for simplicity, I directly passed the value
    with open(f'{file_name}.csv') as crypto_file:

        # Ignoring the first line because it's headers
        next(crypto_file)

        for line_num, line in enumerate(crypto_file, start=1):

            row_values = (line.strip()).split(',')

            for param in dict_with_user_params_and_vals:

                time_delta = 0

                time_interval = dict_with_user_params_and_vals[param][1]
                param_index = dict_with_user_params_and_vals[param][2]

                param_value = row_values[param_index]
                param_datetime = dt.datetime.strptime(row_values[-1], "%Y %m %d - %I:%M:%S %p")                  
                
                # for first line by default, I will add the value since, it will be the basis throug which I will compare the folooowing datetime
                if line_num==1: 
                    params_timeseries_dict_of_dicts[param] = {param_datetime : param_value}
                    # datetime_object : respective_parameter_value_at_that_time

                last_datetime = max(params_timeseries_dict_of_dicts[param].keys())

                # Now for the next values I need to compare if timedelta will be great than the user required, IF yes, I will add it to the dod
                time_delta = param_datetime - last_datetime

                if time_delta.seconds >= time_interval*60:
                    params_timeseries_dict_of_dicts[param].update({param_datetime:param_value})
            
    return params_timeseries_dict_of_dicts

def user_percent_filter(some_dod, dict_with_usr_params_and_vals):
    # some_dod contains paramters as keys and timeseries data at required user intervals as dictionary as values
    percent_filtered_dod = dict() # this will be returned

    for index, params in enumerate(dict_with_usr_params_and_vals):
        user_percent_diff = dict_with_usr_params_and_vals[params][0]
        percent_filtered_dod[params] = {}
        prev_val = None

        for time, value in some_dod[params].items():
            c_value = round(float(value),5)
            
            if prev_val is None:
                prev_val = c_value
                continue
            
            percent_diff = (c_value - prev_val)/prev_val*100
            # print(params, percent_diff, prev_val, c_value, time)
            
            if (user_percent_diff>0 and percent_diff >= user_percent_diff) or \
                (user_percent_diff<0 and percent_diff <= user_percent_diff):
                percent_filtered_dod[params].update({time:[c_value, prev_val, percent_diff]})
                # print(time, c_value, prev_val)
            prev_val = c_value
            # print(prev_val, c_value)
    
    return percent_filtered_dod

def latest_value_filter(dict_with_historical_values):
    lates_value_dict = dict()
    dt_now = dt.datetime(2024, 2, 14, 17, 54, 10)

    for crypto in dict_with_historical_values:
        lates_value_dict[crypto] = {}
        for params in dict_with_historical_values[crypto]:
            try:
                latest_time = max(dict_with_historical_values[crypto][params].keys())   
            except ValueError:
                break
            
            # condition to check if the values is latest according to current time
            if (dt_now - latest_time).seconds < 60:
                latest_value = dict_with_historical_values[crypto][params][latest_time]
                lates_value_dict[crypto].update({params:{latest_time:latest_value}})

    return lates_value_dict

def string_construct(crypto_name, changed_value_dict):
    # print(crypto_name, changed_value_dict)
    string_to_return = ""

    for param in changed_value_dict:
        datetime = list(changed_value_dict[param])[0]
        # print(datetime)
        string_to_return += f"""
        {crypto_name}'s {param} changed by {changed_value_dict[param][datetime][2]} from {changed_value_dict[param][datetime][1]} to {changed_value_dict[param][datetime][0]} at {datetime} """

    print(string_to_return)
    return string_to_return


if __name__ == "__main__":
    start_here(user_crypto_list, user_tracking_dict)

# def time_filter(some_dict, time_interval_in_minutes):
    
#     time_val = [time for time in some_dict]
#     time_interval_in_seconds = time_interval_in_minutes*60
#     time_diff = 0

#     filtered_time = list()
#     filtered_time.append(time_val[0])

#     for i in range(1, len(time_val)):
#         time_diff += (time_val[i] - time_val[i-1]).seconds
#         if time_diff >= time_interval_in_seconds:
#             filtered_time.append(time_val[i])
#             # print(time_diff, time_interval_in_seconds)
#             time_diff = 0
    
#     return filtered_time

# def val_track(some_dict, required_datetime, *args):

#     default_mapper = {
#         'cmcRank':0, 
#         'circulatingSupply':1,
#         'price':2,
#         'volume24':3
#             }

#     user_mapper = {tag:value for tag,value in default_mapper.items() if tag in args}
#     # print(user_mapper)

#     user_required_data_values = [vals for times,vals in some_dict.items() if times in required_datetime]
#     user_required_data_keys = [times for times,vals in some_dict.items() if times in required_datetime]

#     percent_diff_lod = list()

#     len_user_req_data, len_of_val = len(user_required_data_values),len(user_required_data_values[0])

#     for i in range(1,len_user_req_data):
#         temp_list, temp_dict = list(), dict()
#         for k in range(len_of_val):
#             if k in user_mapper.values():
#                 new_data = round(float(user_required_data_values[i][k]),5)
#                 old_data = round(float(user_required_data_values[i-1][k]),5)
#                 temp_list.append(((new_data-old_data)/old_data)*100)
#                 # print(old_data,new_data,temp_dict)
#             temp_dict[user_required_data_keys[i]] = temp_list
#         percent_diff_lod.append(temp_dict)
#         # print(percent_diff_lod)
    
#     return percent_diff_lod

# def trigger_email(some_list_of_dict, *args):

    # params = [val for arg in args for val in arg]

    # for every_dict in some_list_of_dict:
    #     for date_time, values in every_dict.items():
    #         for index, i_values in enumerate(values):
    #             if i_values>params[index]:
    #                 # print(i_values, index, date_time)
    #                 pass