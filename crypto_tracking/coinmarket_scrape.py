import os, requests, json, csv, datetime, time
import config
import common_utilities as cu

# UNCOMMENT THE BELOW CODE ONLY WHEN YOU ARE RUNNING THIS FILE DIRECTLY AND THE CODE AT IF BLOCK BELOW
# pd = os.getcwd()
# try:
#     os.chdir(pd + '/crypto_tracking')
# except FileNotFoundError as e:
#     print(e)


def fetch():
    global fetched_date

    cu.activity_logger('Fetching data')

    # print('Entering_fetch')
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing"
    params = {
        'start':'1',
        'limit':'100',
        'sortBy':'market_cap',
        'sortType':'desc',
        'cryptoType':'all',
        'tagType':'all',
        'audited':'false'
    }
    fetched_date = datetime.datetime.now()

    response = fetch_data(url, params)
    list_of_dict = json_parse(response)
    write_data(list_of_dict)

    # cu.activity_logger('Exited fetch()')

def fetch_data(url, params):
    session = requests.session()

    for _ in range(config.max_retries):
        try:
            response = session.get(url, params=params, timeout=10).json()
            return response
        except TimeoutError as te:
            cu.error_logger(TimeoutError, te)
            print('Retrying after 30 seconds')
            time.sleep(30)
            continue
        except requests.exceptions.ConnectionError as ce:
            cu.error_logger(ConnectionError, ce)
            print(f'{ConnectionError} occurred, retring after 1 minute')
            time.sleep(60)
            continue

    cu.send_email("Hey, \n It seems like we can't fetch data. There might be some connection issues")
    cu.activity_logger("Email sent because of Connectivity Issue")


def json_parse(response_object):
    with open('json_dump.json','w') as file:
        json.dump(response_object,file, indent=4)

    temp_field_names = {'id','name','symbol','cmcRank','circulatingSupply'}
    quotes_field_names = {'price','volume24h','marketCap','marketCapByTotalSupply'}

    data_list_of_dicts = list()

    try:
        os.mkdir('stores')
    except FileExistsError:
        # print('File already exists')
        pass

    with open('json_dump.json','r') as read_file:
        j_file = json.load(read_file)
        crypto_data = j_file['data']['cryptoCurrencyList']
        for crypto in crypto_data:
            # crypto is a dictionary and crypto data is a list of dictonary
            data_storing_dict = {tag:value for tag,value in crypto.items() if tag in temp_field_names}
        
            if 'quotes' in crypto:
                quote_data = crypto['quotes'][0]
                for field, value in quote_data.items():
                    if field in quotes_field_names:
                        data_storing_dict[field] = value
            data_list_of_dicts.append(data_storing_dict)
    
    return data_list_of_dicts


def write_data(some_list_of_dicts):
    global fetched_date

    fields_list = list(some_list_of_dicts[0].keys())

    with open('index.csv','w',encoding='utf-8', newline='') as index:
        index.write(f'Last updated time : {fetched_date.strftime("%B %d, %Y | %I:%M:%S %p")}')
        index.write('\n')
        index = csv.DictWriter(index, fieldnames=fields_list)
        index.writeheader()
        for data in some_list_of_dicts:
            index.writerow(data)

if __name__ == '__main__':
    fetch()
    # os.chdir(pd)