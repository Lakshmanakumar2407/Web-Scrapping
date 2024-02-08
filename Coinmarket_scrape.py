import os, requests, json, csv, datetime


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

session = requests.session()
response = session.get(url, params=params).json()
# print(response.text)

with open('json_dump.json','w') as file:
    json.dump(response,file, indent=4)

temp_field_names = {'id','name','symbol','cmcRank','circulatingSupply'}
quotes_field_names = {'price','volume24h','marketCap','marketCapByTotalSupply'}

data_list_of_dicts = list()

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

fields_list = list(data_list_of_dicts[0].keys())

with open('index.csv','w',encoding='utf-8', newline='') as index:
    index.write(f'Last updated time : {datetime.datetime.now().strftime("%B %d, %Y | %I:%M:%S %p")}')
    index.write('\n')
    index = csv.DictWriter(index, fieldnames=fields_list)
    index.writeheader()
    for data in data_list_of_dicts:
        index.writerow(data)