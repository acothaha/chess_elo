from pathlib import Path 
import pandas as pd
import boto3
import json
from time import time
from prefect import flow, task
from prefect_aws import AwsCredentials

@task(log_prints=True, retries=3)
def lambda_scrape(key: str, secret: str, region: str, n: int=10, aws_client):
    """with AWS lambda Scrape chess data from web and put it in S3"""
    
    
    lambda_client = aws_client.client('lambda')

    test_event = dict({
        'n': n
    })

    response = lambda_client.invoke(
        FunctionName='scrape_elo_chess',
        Payload=json.dumps(test_event),
        InvocationType='Event',
        LogType='Tail'
    )
    
    time.sleep(90 * n)
    
    print("Data is scraped")
    
    return 
    

@task(log_prints=True, retries=3)
def fetch(dataset_url: str, bucket_name: str, aws_client) -> dict:
    """Fetching data from S3 and return it as JSON"""
    
    BUCKET = bucket_name
    PATH = dataset_url
    
    s3_client = aws_client.client('s3')

    content_object = s3_client.get_object(Bucket=BUCKET, Key=PATH) 
    file_content = content_object["Body"].read().decode('utf-8')
    json_content = json.loads(file_content)
    
    return json_content
        
        
@task(log_prints=True, retries=3)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Cleaning the data"""

    player_name = df['white_player'].mode()

    df['play_as'] = df['white_player'].apply(lambda x: play_as_decider(x, player_name[0]))
    df['rating'] = df.apply(lambda x: x['white_player_rating'] if x['play_as'] == 'white' else x['black_player_rating'], axis=1)
    df['opponent'] = df.apply(lambda x: x['white_player'] if x['play_as'] == 'black' else x['black_player'], axis=1)
    df['opponent_rating'] = df.apply(lambda x: x['black_player_rating'] if x['play_as'] == 'white' else x['white_player_rating'], axis=1)
    df['result'] = df.apply(lambda x: chess_result_player(x['play_as'], x['game_result']), axis=1)

    return df[['rating', 'play_as', 'opponent', 'opponent_rating', 'result', 'move', 'ECO', 'site', 'year']]


def chess_result_player(color, result):
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


def play_as_decider(player_name_dependent ,player_name_control):
    try:
        if player_name_dependent == player_name_control:
            return 'white'
        else:
            return 'black'
    except:
        return 'black'

    
@flow
def create_df_from_json(json: dict) -> pd.DataFrame:
    """Create pandas dataframe from JSON"""
    
    list_name = list(json.keys())
    
    df = pd.DataFrame()
    
    for name in list_name:
        df_temp = pd.read_json(json[name])
        df_temp = clean(df_temp)
        df = pd.concat([df, df_temp])
        
    return df

@flow
def write_redshift()