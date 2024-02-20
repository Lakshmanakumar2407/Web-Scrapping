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
import datetime as dt
import common_utilities as cu

# List of Crypto's to track
user_crypto_list = ['Bitcoin', 'Aave', 'Beam', 'Cardano']

# Parameters as key : percent and time interval as key
user_tracking_dict = {'price':[0.1, 10], 'volume24':[1.0, 10]}

# fields available in the stored csv
default_mapper = {
        'cmcRank':0, 
        'circulatingSupply':1,
        'price':2,
        'volume24':3
            }

def analyse_filter(list_of_crypto_to_track, dict_with_params):
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
    cu.activity_logger('Checking data for user changes')

    # print("Entered Store analyse")
    wd = os.getcwd()
    # print(wd)
    path = os.path.join(wd,'stores')
    os.chdir(path)
    # print(os.getcwd())

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

    email_message = ''

    for crypto in dict_with_latest_values:
        if len(dict_with_latest_values[crypto]) != 0:
            email_message += string_construct(crypto, dict_with_latest_values[crypto])

    # print(email_message, len(email_message))
    
    os.chdir(wd)
    # print(os.getcwd())

    # defining this here because of directory stufff
    if len(email_message)!= 0: 
        cu.send_email(email_message)
       
def filter_data_user(file_name, dict_with_user_params_and_vals ):
    '''Dicts values lists first value is percent_inrease, time_interval_minutes, index_of_the_param 
    
    I need to return a dict of dict with dict key being the parameter and value being the time series data
    '''
    params_timeseries_dict_of_dicts = dict()

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
                recorded_time = row_values[-1]
                param_datetime = dt.datetime.strptime(recorded_time, "%Y %m %d - %I:%M:%S %p")                  
                
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
            c_value = round(float(value),20)
            
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
    # dt_now = dt.datetime(2024, 2, 14, 17, 44, 10)
    dt_now = dt.datetime.now()
    # print(dt_now)

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
        percent = round(changed_value_dict[param][datetime][2],3)
        old_value = round(changed_value_dict[param][datetime][1],5)
        new_value = round(changed_value_dict[param][datetime][0],5)

        string_to_return += f"""
        {crypto_name}'s {param} changed by {percent}% from ${old_value} to ${new_value} at {datetime} \n """

    # print(string_to_return)
    return string_to_return


if __name__ == "__main__":
    wd = os.getcwd()
    os.chdir(wd+'\\crypto_tracking\\Stores')
    user_crypto_list1 = [file.split('.')[0] for file in os.listdir()]
    os.chdir(wd)

    analyse_filter(user_crypto_list1, user_tracking_dict)