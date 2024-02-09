import os, csv, pytz
import datetime as dt 

def main():
    local_time = pytz.timezone('Asia/Kolkata')

    wd = os.getcwd()
    # if os.getcwd() != os.getcwd()+'/Stores':
    os.chdir(os.getcwd()+'/Stores')

    try: 
        with open('index.csv') as index:
            next(index)
            index_reader = csv.DictReader(index)
            
            choosen_field = ['cmcRank','price','circulatingSupply','volume24h']

            for index, diction in enumerate(index_reader, start=1):
                file_name = diction.get('name','')
                temp_diction = {tag:value for tag,value in diction.items() if tag in choosen_field}
                temp_diction.update({'fetched_on':dt.datetime.now().astimezone(local_time).strftime("%Y %m %d - %I:%M:%S %p")})
                field_head = list(temp_diction.keys())
                
                if index == 1: 
                    # print(temp_diction,field_head)
                    if not os.path.isfile(f'{file_name}.csv') or os.path.getsize(f'{file_name}.csv') == 0:
                        with open(f'{file_name}.csv','w',newline='') as writer:
                            writer_csv = csv.DictWriter(writer,fieldnames=field_head)
                            writer_csv.writeheader()
                    with open(f'{file_name}.csv','a',newline='') as writer:
                            writer_csv = csv.DictWriter(writer,fieldnames=field_head)
                            writer_csv.writerow(temp_diction)

    except FileNotFoundError :
        print('File not Found')
    finally:
        os.chdir(wd)

if __name__ == '__main__':
    main()