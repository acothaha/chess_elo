import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
import json
from urllib.request import Request, urlopen
from io import StringIO, BytesIO
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import boto3
import datetime
from PIL import Image

st.set_page_config(
    layout="wide",
    page_title="Head to Head",
    page_icon="⚔️",
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
.right_name {
    font-family: Noto Sans;
    font-weight: bold;
    font-size: 40px;
    text-align: right;
}
.left_name {
    font-family: Noto Sans;
    font-weight: bold;
    font-size: 40px;
    text-align: left;
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





st.markdown('''
    <div class="first_title">
       ⚔️Head to Head⚔️
    </div>
    ''', unsafe_allow_html=True)


# c1, c2 = st.columns((3, 2))
# with c2:
#     st.write("##")
#     st.write("##")
#     st.markdown("hilih kindsfgsdfredsvnuhviufhviuhduvhaeiurhvidshvihfduhvifhvuidhfsvihuierhvudsbvuab")
# st.write("##")
# with c1:
#     st.write("##")
#     st.write("##")
#     st.markdown(
#         '<p class="intro">Bienvenue sur la <b>no-code AI platform</b> ! Déposez vos datasets csv ou excel ou choisissez en un parmi ceux proposés et commencez votre analyse dès maintenant ! Cherchez les variables les plus intéressantes, visualisez vos données, et créez vos modèles de Machine Learning en toute simplicité.' +
#         ' Si vous choisissez de travailler avec votre dataset et que vous voulez effectuez des modifications sur celui-ci, il faudra le télécharger une fois les modifications faites pour pouvoir l\'utiliser sur les autres pages. </p>',
#         unsafe_allow_html=True)
#     st.markdown(
#         '<p class="intro">Un tutoriel sur l\'utilisation de ce site est disponible sur le repo Github. En cas de bug ou d\'erreur veuillez m\'en informer par mail ou sur Discord.</p>',
#         unsafe_allow_html=True)
#     st.markdown(
#         '<p class="intro"><b>Commencez par choisir un dataset dans la section Dataset !</b></p>',
#         unsafe_allow_html=True)

# ## get 

credentials = service_account.Credentials.from_service_account_file('cred_google.json')
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

df = client.query(sql).to_dataframe()

## fetch bio data

cred = []

with open('credentials.txt') as f:
    for row in f:
        cred.append(row.rstrip('\n'))

date_choose = datetime.datetime.today().strftime('%Y-%m-%d')
# date_choose = '2023-05-26'

BUCKET = 'chess-elo-bucket'

s3_client = boto3.client(
    "s3",
    aws_access_key_id=cred[0],
    aws_secret_access_key=cred[1]
)

get_file_s3 = s3_client.list_objects(Bucket=BUCKET, Delimiter='/', Prefix='data_json/')

choose_date_path = get_file_s3['CommonPrefixes'][-1]['Prefix']

PATH = f'{choose_date_path}chess_bio.json'

content_object = s3_client.get_object(Bucket=BUCKET, Key=PATH)

file_content = content_object["Body"].read().decode('utf-8')
bio_content = json.loads(file_content)

## display

name = (df.sort_values(by='ranking')['player_name']).unique()


placeholder_left = st.sidebar.empty()

placeholder_right = st.sidebar.empty()

pick_name_left = placeholder_left.selectbox('Choose 1st Player', name, key='left_selectbox')

pick_name_right = placeholder_right.selectbox('Choose 2nd Player', name[name != pick_name_left], key='right_selectbox')

bio_pick_left = bio_content[pick_name_left]
bio_pick_right = bio_content[pick_name_right]

c_name_left, c_name_right = st.columns(2)

df_pick = df.loc[(df['player_name'] == pick_name_left) & (df['opponent'] == pick_name_right)].reset_index(drop=True)


with c_name_left:
    st.text('')
    st.markdown(f'''
        <p class="left_name">{pick_name_left}🔴</p>
        ''', unsafe_allow_html=True)
    
    
    
    

    
with c_name_right:
    st.text('')
    st.markdown(f'''
        <p class="right_name">🔵{pick_name_right}</p>
        ''', unsafe_allow_html=True)
    
    

c_info_left, c_info_center, c_info_right = st.columns([1,1,1])

with c_info_left:
    st.markdown(
    f"""
    <div style="text-align: left"><img src={bio_pick_left['image']} width="200" alt="My Image" /></div>
    """, unsafe_allow_html=True
    )

    with st.columns(2)[0]:
        st.text('')
        placeholder_left_color = st.empty()
    
with c_info_right:
    st.markdown(
    f"""
    <div style="text-align: right;"><img src={bio_pick_right['image']} width="200" alt="My Image" /></div>
    """, unsafe_allow_html=True
    )
    with st.columns(2)[-1]:
        st.text('')
        placeholder_right_color = st.empty()


left_color = placeholder_left_color.select_slider('', options=['⚪White', 'All', '⚫Black'], label_visibility='collapsed', value='All', key='left_color_select')



if left_color == 'All':
    right_color = placeholder_right_color.select_slider('', options=['⚪White', 'All', '⚫Black'], value='All', label_visibility='collapsed', key='right_color_select_all', disabled=True )
            
elif left_color == '⚫Black':
    right_color = placeholder_right_color.select_slider('', options=['⚪White', 'All', '⚫Black'], value='⚪White', label_visibility='collapsed', key='right_color_select_white', disabled=True )

elif left_color == '⚪White':
    right_color = placeholder_right_color.select_slider('', options=['⚪White', 'All', '⚫Black'], value='⚫Black', label_visibility='collapsed', key='right_color_select_black', disabled=True )


color_dict = {
    'All': ['white', 'black'],
    '⚫Black': ['black'],
    '⚪White': ['white'],
}

df_pick_colored = df_pick.loc[df_pick['play_as'].isin(color_dict[left_color])]

# if 'left_color' not in st.session_state:
#     st.session_state.left_color = 'All'

# if 'right_color' not in st.session_state:
#     st.session_state.right_color = 'All'
    
# if 'left_color_index' not in st.session_state:
#     st.session_state.left_color_index = 0

# if 'right_color_index' not in st.session_state:
#     st.session_state.right_color_index = 0

# st.text(st.session_state.left_color_index)
# st.text(st.session_state.right_color_index)

# left_color = placeholder_left_color.selectbox('Choose 1st Player', ['All', 'White', 'Black'], key='left_color_selectbox', label_visibility='hidden', index=st.session_state.left_color_index)
# right_color = placeholder_right_color.selectbox('Choose 2nd Player', ['All', 'White', 'Black'], key='right_color_selectbox', label_visibility='hidden', index=st.session_state.right_color_index)

# left_color = placeholder_left_color.selectbox('Choose 1st Player', ['All', 'White', 'Black'], key='left_color_selectbox_2nd', label_visibility='hidden')
# right_color = placeholder_right_color.selectbox('Choose 2nd Player', ['All', 'White', 'Black'], key='right_color_selectbox_2nd', label_visibility='hidden')

# if left_color != st.session_state.left_color:
#     if left_color == 'All':
#         right_color = placeholder_right_color.selectbox('Choose 2nd Player', ['All', 'White', 'Black'], key='right_color_selectbox_all', label_visibility='hidden', index=0)
#         st.session_state.left_color = 'All'
#         st.session_state.right_color = 'All'
#         st.session_state.left_color_index = 0
#         st.session_state.right_color_index = 0
    
#     elif left_color == 'White':
#         right_color = placeholder_right_color.selectbox('Choose 2nd Player', ['All', 'White', 'Black'], key='right_color_selectbox_black', label_visibility='hidden', index=2)
#         st.session_state.left_color = 'White'
#         st.session_state.right_color = 'Black'
#         st.session_state.left_color_index = 1
#         st.session_state.right_color_index = 2
         
#     elif left_color == 'Black':
#         right_color = placeholder_right_color.selectbox('Choose 2nd Player', ['All', 'White', 'Black'], key='right_color_selectbox_white', label_visibility='hidden', index=1)
#         st.session_state.left_color = 'Black'
#         st.session_state.right_color = 'White'
#         st.session_state.left_color_index = 2
#         st.session_state.right_color_index = 1
        
# elif right_color != st.session_state.right_color:
#     if right_color == 'All':
#         left_color = placeholder_left_color.selectbox('Choose 2nd Player', ['All', 'White', 'Black'], key='right_color_selectbox_all', label_visibility='hidden', index=0)
#         st.session_state.left_color = 'All'
#         st.session_state.right_color = 'All'
#         st.session_state.left_color_index = 0
#         st.session_state.right_color_index = 0
    
#     elif right_color == 'Black':
#         left_color = placeholder_left_color.selectbox('Choose 2nd Player', ['All', 'White', 'Black'], key='right_color_selectbox_black', label_visibility='hidden', index=1)
#         st.session_state.left_color = 'White'
#         st.session_state.right_color = 'Black'
#         st.session_state.left_color_index = 1
#         st.session_state.right_color_index = 2
           
#     elif right_color == 'White':
#         left_color = placeholder_left_color.selectbox('Choose 2nd Player', ['All', 'White', 'Black'], key='right_color_selectbox_white', label_visibility='hidden', index=2)
#         st.session_state.left_color = 'Black'
#         st.session_state.right_color = 'White'
#         st.session_state.left_color_index = 2
#         st.session_state.right_color_index = 1

# else:
#     pass


st.dataframe(df_pick_colored)