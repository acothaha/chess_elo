import re
import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
from tqdm import tqdm
from time import time
from datetime import datetime
from pathlib import Path
import s3fs

def get_cred(cred_path='credentials.txt'):
    cred = []

    with open(cred_path) as f:
        for row in f:
            cred.append(row.rstrip('\n'))

    return cred

def main(path_init='data', n=100):

    name_list_dict = name_list(n)
    date = datetime.today().strftime('%Y-%m-%d')
    path = f"{path_init}/{date}"

    # Path(path).mkdir(parents=True, exist_ok=True)

    for values in name_list_dict.values():
        temp = Chess_Elo(list(name_list_dict.keys()), values[0], values[-1], path)
        temp.df_elo()

    temp.df_ranking()
    


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
    def __init__(self, ranking, name, url, path):
        self.ranking = ranking
        self.name = name
        self.url = url
        self.path = path
        self.n = 0
        self.cred_list = get_cred()

    def tqdm_generator(self):
        while True:
            yield

    def chess_result_player(self, color, result):
        game_result = result.split('-')
        if color == 'white':
            if game_result[0] == '1':
                return 'win'
            elif game_result[0] == '0':
                return 'lose'
            else:
                return 'draw'
        else:
            if game_result[1] == '1':
                return 'win'
            elif game_result[1] == '0':
                return 'lose'
            else:
                return 'draw'

    def scrape_chess_elo(self):

        df_temp = pd.DataFrame(columns=['game_id', 
                                        'white_player', 
                                        'white_player_rating',
                                        'black_player',
                                        'black_player_rating',
                                        'game_result',
                                        'move',
                                        'ECO',
                                        'site',
                                        'year'])

        for _ in tqdm(self.tqdm_generator()):
            self.n += 1
            begin = len(df_temp)
           
            
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
                    df_temp.loc[len(df_temp)] = lst
                except:
                    try:
                        if bool(re.search('^[A-Z]{1}[0-9]{2}$', lst[7])):
                            lst.insert(8, None)
                            df_temp.loc[len(df_temp)] = lst
                        else:
                            lst.insert(7, None)
                            df_temp.loc[len(df_temp)] = lst
                    except:
                        lst.insert(7, None)
                        df_temp.loc[len(df_temp)] = lst
            
            if begin == len(df_temp):
                break
            else:
                pass

        return df_temp

    def play_as_decider(self, player_name_dependent ,player_name_control):
        try:
            if player_name_dependent == player_name_control:
                return 'white'
            else:
                return 'black'
        except:
            return 'black'


    def df_ranking(self):

        pd.DataFrame(self.ranking, columns=['name']).to_csv(
                                                        f'{self.path}/rankings.csv', 
                                                        index=False, 
                                                        storage_options={
                                                            'key': self.cred_list[0],
                                                            'secret': self.cred_list[1]
                                                        })

    def df_elo(self):

        df = self.scrape_chess_elo().copy()
        player_name = df['white_player'].mode()

        df['play_as'] = df['white_player'].apply(lambda x: self.play_as_decider(x, player_name[0]))
        df['rating'] = df.apply(lambda x: x['white_player_rating'] if x['play_as'] == 'white' else x['black_player_rating'], axis=1)
        df['opponent'] = df.apply(lambda x: x['white_player'] if x['play_as'] == 'black' else x['black_player'], axis=1)
        df['opponent_rating'] = df.apply(lambda x: x['black_player_rating'] if x['play_as'] == 'white' else x['white_player_rating'], axis=1)
        df['result'] = df.apply(lambda x: self.chess_result_player(x['play_as'], x['game_result']), axis=1)


        df[['rating', 'play_as', 'opponent', 'opponent_rating', 'result', 'move', 'ECO', 'site', 'year']].to_csv(
                                                                                                            f'{self.path}/{self.name}.csv', 
                                                                                                            index=False, 
                                                                                                            storage_options={
                                                                                                                'key': self.cred_list[0],
                                                                                                                'secret': self.cred_list[1]
                                                                                                            })



print('Loading function')

def lambda_handler(event, context):

    with open('bucket_url.txt') as f:
        bucket_url = f.readlines()[0]
    #print("Received event: " + json.dumps(event, indent=2))

    n = event['n']

    main(bucket_url, n)