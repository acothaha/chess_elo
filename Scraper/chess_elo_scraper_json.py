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

def main(s3_client, date, path_init='data', n=100):

    name_list_dict = fetch_ranking_from_s3(date)

    json_result = {}

    # Path(path).mkdir(parents=True, exist_ok=True)

    for name, values in list(name_list_dict.items())[:n]:
        
        temp = Chess_Elo(values[0], values[-1])
        json_result[name] = temp.scrape_chess_elo()
        path = f"{path_init}/{date}/{name}.json"


    response = s3_client.put_object( 
            Bucket='chess-elo-bucket',
            Body=(bytes(json.dumps(json_result).encode('UTF-8'))),
            Key=f'{path}'
        )
    


def fetch_ranking_from_s3(date_choose: str) -> dict:
    """Fetching data from S3 and return it as JSON"""
    
    BUCKET = 'chess-elo-bucket'
    PATH = f'data_json/{date_choose}/ranking.json'
    
    cred = get_cred()
    
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=cred[0],
        aws_secret_access_key=cred[1]
    )

    content_object = s3_client.get_object(Bucket=BUCKET, Key=PATH)

    file_content = content_object["Body"].read().decode('utf-8')
    json_content = json.loads(file_content)
    
    return json_content


class Chess_Elo(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
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
            'year': [],
            'date': []
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
                    
            for row in result:
                lst = []
                for k in row.split('><'):
                    try:
                        val_temp = re.search(r'>(.*)<', k).group(1)
                        if val_temp == ' ':
                            lst.append(None)
                        else:
                            lst.append(val_temp)
                    except: 
                        pass
                
                if len(json_temp)-1 == len(lst):
                    pass
                
                else:
                    try:
                        if bool(re.search('^[A-Z]{1}[0-9]{2}$', lst[7])):
                            lst.insert(8, None)
    
                        else:
                            lst.insert(7, None)
    
                    except:
                        lst.insert(7, None)
                
                try:
                    lst.append(re.search('\d{4}-\d{2}-\d{2}', row).group(0))
                except:
                    lst.append(None)
                    
                for i, val in zip(list(json_temp.keys()), lst):
                    json_temp[i].append(val)
            
            if begin == len(json_temp['game_id']):
                break
            else:
                pass
        
        return json_temp




def lambda_handler(event, context):

    # date = datetime.today().strftime('%Y-%m-%d')
    date = '2023-05-24'

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

    main(s3_client, date, bucket_url, n)
