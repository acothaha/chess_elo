import re
import json
from urllib.request import Request, urlopen
from tqdm import tqdm
from time import time
from datetime import datetime
from pathlib import Path
import boto3



def get_cred(cred_path='credentials.txt'):
    cred = []

    with open(cred_path) as f:
        for row in f:
            cred.append(row.rstrip('\n'))

    return cred

def main(s3_client, path_init='data', n=100):

    name_list_dict = name_list(n)
    date = datetime.today().strftime('%Y-%m-%d')
    path = f"{path_init}/{date}.json"
    json_result = {}

    # Path(path).mkdir(parents=True, exist_ok=True)

    for name, values in zip(name_list_dict.keys(), name_list_dict.values()):
        
        temp = Chess_Elo(values[0], values[-1], path)
        json_result[name] = temp.scrape_chess_elo()


    response = s3_client.put_object( 
            Bucket='chess-elo-bucket',
            Body=(bytes(json.dumps(json_result).encode('UTF-8'))),
            Key=f'{path}'
        )
    


def name_list(n):
    url=f"https://2700chess.com/?per-page=100"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})


    while True:
        try:
            web_byte = urlopen(req).read()
            break
        except:
            time.sleep(1)

    webpage = web_byte.decode('utf-8')

    result_url = re.findall('(?<=search=)(.*)(?=" title=")', webpage)[:n]
    result_file_name = re.findall('(?<=<a href="/players/)(.*)(?=">)', webpage)[:n]
    result_name = []
    for name in result_file_name:
        result_name.append(re.findall(f'(?<=<a href="/players/{name}">)(.*)(?=</a>)', webpage)[0])

    result_dict = dict(zip(result_name, list(zip(result_file_name, result_url))))

    return result_dict


class Chess_Elo(object):
    def __init__(self, name, url, path):
        self.name = name
        self.url = url
        self.path = path
        self.n = 0

    def tqdm_generator(self):
        while True:
            yield

    def scrape_chess_elo(self):
        json_temp = {
            'game_id': [], 
            'white_player': [], 
            'white_player_rating': [],
            'black_player': [],
            'black_player_rating': [],
            'game_result': [],
            'move': [],
            'ECO': [],
            'site': [],
            'year': []
        }

        for _ in tqdm(self.tqdm_generator()):
            self.n += 1

            begin = len(json_temp['game_id'])
    
    
            url=f"https://2700chess.com/games?search={self.url}&page={self.n}"
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

            while True:
                try:
                    web_byte = urlopen(req).read()
                    break
                except:
                    time.sleep(1)

            webpage = web_byte.decode('utf-8')
                    
            result = re.findall('tr data-key(.*)tr', webpage)
                    
            for i in result:
                lst = []
                for k in i.split('><'):
                    try:
                        val_temp = re.search(r'>(.*)<', k).group(1)
                        if val_temp == ' ':
                            lst.append(None)
                        else:
                            lst.append(val_temp)
                    except: 
                        pass

                try:
                    if bool(re.search('^[A-Z]{1}[0-9]{2}$', lst[7])):
                        lst.insert(8, None)

                    else:
                        lst.insert(7, None)

                except:
                    lst.insert(7, None)

                
                for i, val in zip(list(json_temp.keys()), lst):
                    json_temp[i].append(val)
            
            if begin == len(json_temp['game_id']):
                break
            else:
                pass
        
        return json_temp



    def df_ranking(self):

        pd.DataFrame(self.ranking, columns=['name']).to_csv(
                                                        f'{self.path}/rankings.csv', 
                                                        index=False, 
                                                        storage_options={
                                                            'key': self.cred_list[0],
                                                            'secret': self.cred_list[1]
                                                        })



print('Loading function')

def lambda_handler(event, context):

    cred = get_cred()

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=cred[0],
        aws_secret_access_key=cred[1]
    )

    with open('bucket_url.txt') as f:
        bucket_url = f.readlines()[0]
    #print("Received event: " + json.dumps(event, indent=2))

    n = event['n']

    main(s3_client, bucket_url, n)

lambda_handler({'n': 1}, None)