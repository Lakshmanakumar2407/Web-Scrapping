import os
import datetime as dt
# from memory_profiler import profile


def price_track(some_list, percent, time_period):
    list_len = len(some_list)
    price_delta = [(float(some_list[i])-float(some_list[i-1]))/float(some_list[i-1])*100 for i in range(1,list_len)]
    delta_dict = {}
    for index, delta in enumerate(price_delta, start=1):
        if delta>percent:
            delta_dict[index] = delta
            # print(delta, index, some_list.index(some_list[index]), some_list[index])
    return delta_dict

def time_filter(some_dict, time_interval_in_minutes):
    time_val = [time for time in some_dict]

    filtered_time = list()
    filtered_time.append(time_val[0])

    for i in range(1, len(time_val)):
        time_diff = time_val[i] - time_val[i-1]
        print(time_diff.seconds)

# @profile
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
            cmcRank, circulatingSupply, price, volume24, datetime_str = row_values

            dict_with_datetime_as_key.update(
                {dt.datetime.strptime(datetime_str,"%Y %m %d - %I:%M:%S %p"):[cmcRank,circulatingSupply,price,volume24]})

            cmcRank_list.append(cmcRank)
            circulatingSupply_list.append(circulatingSupply)
            price_list.append(price)
            volume24_list.append(volume24)
            datetime_list.append(dt.datetime.strptime(datetime_str,"%Y %m %d - %I:%M:%S %p"))

        # print(dict_with_datetime_as_key)
    # return_dict = price_track(price_list,0.1,3600)
    # for key, value in return_dict.items():
    #     # print(f'''The stock rose by {value}% at time {datetime_list[key]}
              
    #     #         Other Stock details at that time 
    #     #         Stock price = {price_list[key]}
    #     #         circulating Supple = {circulatingSupply_list[key]}\n\n''')
    #     pass
        
        time_filter(dict_with_datetime_as_key,20)
    

if __name__ == "__main__":
    start_here()