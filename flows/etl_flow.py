from pathlib import Path 
import requests
import pandas as pd
import boto3
import json
from datetime import date
import time
from tqdm import tqdm
from prefect import flow, task
from prefect_aws import AwsCredentials
from prefect_gcp import GcpCredentials

@task(log_prints=True, retries=3)
def lambda_scrape(n: int=1) -> None:
    """with AWS lambda Scrape chess data from web and put it in S3"""
    
    aws_credentials_block = AwsCredentials.load("chess-elo-cred")
    
    s3_session = aws_credentials_block.get_boto3_session()
    
    lambda_client = s3_session.client('lambda')

    test_event = dict({
        'n': n
    })

    response = lambda_client.invoke(
        FunctionName='scrape_elo_chess',
        Payload=json.dumps(test_event),
        InvocationType='Event',
        LogType='Tail'
    )
    
    for i in tqdm(range(200)):
        time.sleep(1)
    
    print("Data is scraped")
    
@task(log_prints=True, retries=3)
def lambda_ranking(n: int=100) -> None:
    """with AWS lambda Scrape chess data from web and put it in S3"""
    
    aws_credentials_block = AwsCredentials.load("chess-elo-cred")
    
    s3_session = aws_credentials_block.get_boto3_session()
    
    lambda_client = s3_session.client('lambda')

    test_event = dict({
        'n': n
    })

    response = lambda_client.invoke(
        FunctionName='chess_elo_ranking',
        Payload=json.dumps(test_event),
        InvocationType='Event',
        LogType='Tail'
    )

    for i in tqdm(range(10)):
        time.sleep(1)
    
    print("Ranking is scraped")

@task(log_prints=True, retries=3)
def lambda_bio(n: int=100) -> None:
    """with AWS lambda Scrape chess data from web and put it in S3"""
    
    aws_credentials_block = AwsCredentials.load("chess-elo-cred")
    
    s3_session = aws_credentials_block.get_boto3_session()
    
    lambda_client = s3_session.client('lambda')

    test_event = dict({
        'n': n
    })

    response = lambda_client.invoke(
        FunctionName='chess_bio',
        Payload=json.dumps(test_event),
        InvocationType='Event',
        LogType='Tail'
    )

    for i in tqdm(range(10)):
        time.sleep(1)
    
    print("Ranking is scraped")
    

@task(log_prints=True, retries=3)
def fetch_ranking_from_s3(date_choose: str) -> dict:
    """Fetching data from S3 and return it as JSON"""
    
    BUCKET = 'chess-elo-bucket'
    PATH = f'data_json/{date_choose}/ranking.json'
    
    aws_credentials_block = AwsCredentials.load("chess-elo-cred")
    
    s3_session = aws_credentials_block.get_boto3_session()

    s3_client = s3_session.client('s3')

    content_object = s3_client.get_object(Bucket=BUCKET, Key=PATH) 
    file_content = content_object["Body"].read().decode('utf-8')
    json_content = json.loads(file_content)

    return json_content

@task(log_prints=True, retries=3)
def fetch_elo_from_s3(date_choose: str, name: str) -> dict:
    """Fetching data from S3 and return it as JSON"""
    
    BUCKET = 'chess-elo-bucket'
    PATH = f'data_json/{date_choose}/{name}.json'
    print(PATH)
    aws_credentials_block = AwsCredentials.load("chess-elo-cred")
    
    s3_session = aws_credentials_block.get_boto3_session()

    s3_client = s3_session.client('s3')

    content_object = s3_client.get_object(Bucket=BUCKET, Key=PATH) 
    file_content = content_object["Body"].read().decode('utf-8')
    json_content = json.loads(file_content)
    
    return json_content
        
        
@task(log_prints=True, retries=3)
def clean(df: pd.DataFrame, n:int) -> pd.DataFrame:
    """Cleaning the data"""

    player_name = df['white_player'].mode()

    df['player_name'] = player_name[0]
    df['ranking'] = n+1
    df['play_as'] = df['white_player'].apply(lambda x: play_as_decider(x, player_name[0]))
    df['rating'] = df.apply(lambda x: x['white_player_rating'] if x['play_as'] == 'white' else x['black_player_rating'], axis=1)
    df['opponent'] = df.apply(lambda x: x['white_player'] if x['play_as'] == 'black' else x['black_player'], axis=1)
    df['opponent_rating'] = df.apply(lambda x: x['black_player_rating'] if x['play_as'] == 'white' else x['white_player_rating'], axis=1)
    df['result'] = df.apply(lambda x: chess_result_player(x['play_as'], x['game_result']), axis=1)
    df['rn'] = range(1, df.shape[0]+1)
    return df[['player_name', 'ranking', 'rating', 'play_as', 'opponent', 'opponent_rating', 'result', 'move', 'site', 'date', 'rn']]


def chess_result_player(color: str, result: str) -> str:
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


def play_as_decider(player_name_dependent: str ,player_name_control: str) -> str:
    try:
        if player_name_dependent == player_name_control:
            return 'white'
        else:
            return 'black'
    except:
        return 'black'


@task(log_prints=True, retries=3)
def write_to_bq(df: pd.DataFrame) -> None:
    """Write data into BigQuery from dataframe"""

    gcp_credentials_block = GcpCredentials.load("zoomcamp-gcp-creds")

    df.to_gbq(
        destination_table='chess_elo.players',
        project_id='esoteric-code-377203',
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=1000,
        if_exists='replace'
    )

    # bq_client = gcp_credentials_block.get_bigquery_client()

    # job = bq_client.load_table_from_dataframe(
    #     df, 
    #     'chess_elo.players')
    # print(job.result())


    # pandas_gbq.to_gbq(
    #     df, 
    #     destination_table='chess_elo.players',
    #     project_id='esoteric-code-377203',
    #     credentials=gcp_credentials_block.get_credentials_from_service_account(),
    #     chunksize=1000,
    #     if_exists='replace')

@task(log_prints=True, retries=3)
def invoke_dbt(df: pd.DataFrame) -> None:
    """Write data into BigQuery from dataframe"""

    job_id = '300681'
    account_id = '149500'
    api_key = 'b8ebe8ac1f515859695bfee398aadb3200b96a2c'

    url = f'https://cloud.getdbt.com/api/v2/accounts/149500/jobs/{job_id}/run/'
    myobj = {'somekey': 'somevalue'}

    x = requests.post(url, json = myobj)

@flow()
def create_df_from_json(json_data) -> pd.DataFrame:
    """Create pandas dataframe from JSON"""
    
    list_name = list(json_data.keys())
    
    df = pd.DataFrame()
    
    for n, name in enumerate(list_name):
        df_temp = pd.DataFrame(json_data[name])
        df_temp = clean(df_temp, n)
        df = pd.concat([df, df_temp])
        
    
    return df


@flow()
def etl_s3_to_gcs(date):

    json_temp = {}
    ranking = fetch_ranking_from_s3(date)

    for key, value in zip(ranking.keys(), ranking.values()):
        json_data = fetch_elo_from_s3(date, value[0])
        json_temp[key] = json_data[key]
    
    df = create_df_from_json(json_temp)
    write_to_bq(df)

@flow()
def chess_elo_parent_flow(url, n):

    lambda_ranking(n)

    lambda_bio(n)

    for i in range(n):
        lambda_scrape(i+1)

    

    etl_s3_to_gcs(url)

if __name__ == '__main__':

    date_today = str(date.today())
    # date_today = '2023-05-23'
    n = 10

    chess_elo_parent_flow(date_today, n)



