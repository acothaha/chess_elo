import streamlit as st
import base64
import json
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import boto3
import datetime


st.set_page_config(
    layout="wide",
    page_title="Main Page",
    page_icon="👋🏼",
)


# CSS style
st.markdown('''
<style>
.first_title {
    font-family: Helvetica;
    font-weight: bold;
    font-size: 75px;
    text-align: center;
}
.intro {
    font-size: 20px !important;
    text-align: justify;
}
.title {
    font-size:40px !important;
    font-weight: bold;
    text-align: center;
    text-decoration: underline;
    text-decoration-color: #4976E4;
    text-decoration-thickness: 5px;
    width: 100%;
}
.dashboard_title {
font-size: 20px !important;
font-weight: bold;
text-align: right;
}


</style>
''', unsafe_allow_html=True)


st.write("# Welcome to Top 10 Chess Player Dashboard 👋🏼")

st.markdown(
    """
    Hello 👋🏼👋🏼👋🏼!! Aco here!! This is the Final product of my Data Engineering Project. I built a dashboard with Streamlit to display the Top 10 Chess player statistics
    and their head to head statistics. some of the graphs that are shown in the dashboards are interactive, so make sure to hover
    over it 😁😁. 
    
    **🖱️ Click [HERE](https://github.com/acothaha/chess_elo)** for detail of the project

    **👈 Select a tab on the sidebar** to get started!!!

    
    ### Want to see my other projects?
    - Machine Learning + Neural Network 💁 [Customer Churn Prediction](https://github.com/acothaha/Customer-Churn-Prediction)
    - A/B Testing 🐈 [Cookie Cats](https://github.com/acothaha/Mobile-Games-A-B-Testing---Cookie-Cats)
    - Data Analysis + Data Visualization 🍃 [Market Expansion](https://github.com/acothaha/WEED-market-expansion)
    ### Check out my Social Media
    <div style="float: left;"><img src="https://cdn1.iconfinder.com/data/icons/logotypes/32/circle-linkedin-512.png" width="15" height="15"/>&nbsp&nbsp<a href="https://www.linkedin.com/in/acothaha/?locale=en_US">Linkedin</a></div>       
    
""", unsafe_allow_html=True)

st.markdown("""
    <div style="float: left;"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="15" height="15"/>&nbsp&nbsp<a href="https://github.com/acothaha">Github</a></div>          
            """, unsafe_allow_html=True)



if 'df' not in st.session_state:

    cred_google = {
        "type": st.secrets["google"]["type"],
        "project_id": st.secrets["google"]["project_id"],
        "private_key_id": st.secrets["google"]["private_key_id"],
        "private_key": st.secrets["google"]["private_key"],
        "client_email": st.secrets["google"]["client_email"],
        "client_id": st.secrets["google"]["client_id"],
        "auth_uri": st.secrets["google"]["auth_uri"],
        "token_uri": st.secrets["google"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["google"]["client_x509_cert_url"],
        "universe_domain": st.secrets["google"]["universe_domain"]
    }



    credentials = service_account.Credentials.from_service_account_info(cred_google)
    project_id = 'esoteric-code-377203'

    client = bigquery.Client(credentials=credentials, project=project_id)

    sql = """
        SELECT 
            player_name,
            ranking, 
            rating,
            play_as,
            opponent,
            opponent_rating,
            result,
            move,
            site,
            date,
            rn
        FROM 
            `esoteric-code-377203.chess_elo_production.chess_elo_top`
        ORDER BY 
            ranking, rn
        """

    st.session_state.df = client.query(sql).to_dataframe()
    
if 'bio_content' not in st.session_state:
    ## fetch bio data

    cred_aws = [st.secret["aws"]["access_id"], st.secret["aws"]["access_key"]]

    BUCKET = 'chess-elo-bucket'

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=cred_aws[0],
        aws_secret_access_key=cred_aws[1]
    )

    get_file_s3 = s3_client.list_objects(Bucket=BUCKET, Delimiter='/', Prefix='data_json/')

    choose_date_path = get_file_s3['CommonPrefixes'][-1]['Prefix']

    PATH = f'{choose_date_path}chess_bio.json'

    content_object = s3_client.get_object(Bucket=BUCKET, Key=PATH)

    file_content = content_object["Body"].read().decode('utf-8')

    st.session_state.bio_content = json.loads(file_content)
    



