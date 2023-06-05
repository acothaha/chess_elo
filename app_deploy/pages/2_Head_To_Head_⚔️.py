import streamlit as st
import base64
import json
from urllib.request import Request, urlopen
from io import StringIO, BytesIO
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
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

if 'df' not in st.session_state:
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

    st.session_state.df = client.query(sql).to_dataframe()
    
if 'bio_content' not in st.session_state:
    cred = []

    with open('credentials.txt') as f:
        for row in f:
            cred.append(row.rstrip('\n'))

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

    st.session_state.bio_content = json.loads(file_content)
    


## fetch bio data



df = st.session_state.df

bio_content = st.session_state.bio_content

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
    
    

c_info_left, c_info_center, c_info_right = st.columns([1,2,1])

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


with c_info_center:
    
    c1, c2, c3 = st.columns([3,3,3])
    
    with c2:
        
        st.markdown(
            f"""
            <p style="font-size: 20px; font-weight: bold;text-align: center;">Title</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="font-size: 20px; font-weight: bold;text-align: center;">World Ranking</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="font-size: 20px; font-weight: bold;text-align: center;">Live Rating</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="font-size: 20px; font-weight: bold;text-align: center;">FIDE Rating</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="font-size: 20px; font-weight: bold;text-align: center;">Result</p>
            """, unsafe_allow_html=True
            )

    with c3:
        
        st.markdown(
            f"""
            <p style="text-align: left; font-size: 20px;">{bio_pick_right['title']}</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="text-align: left; font-size: 20px;">{bio_pick_right['world']}</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="text-align: left; font-size: 20px;">{bio_pick_right['live_rating']}</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="text-align: left; font-size: 20px;">{bio_pick_right['FIDE_rating']}</p>
            """, unsafe_allow_html=True
            )


        
        
    with c1:
        
        st.markdown(
            f"""
            <p style="text-align: right; font-size: 20px;">{bio_pick_left['title']}</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="text-align: right; font-size: 20px;">{bio_pick_left['world']}</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="text-align: right; font-size: 20px;">{bio_pick_left['live_rating']}</p>
            """, unsafe_allow_html=True
            )
        
        st.markdown(
            f"""
            <p style="text-align: right; font-size: 20px;">{bio_pick_left['FIDE_rating']}</p>
            """, unsafe_allow_html=True
            )

    
 
    try:
        
        df_pie = df_pick_colored['result'].value_counts().reset_index().sort_values('result')
        
        arr = np.array(df_pie['count'])
        
        arr = arr/arr.sum() * 100
        
        fig, ax = plt.subplots(figsize=(20,1.5))
        
        ax.barh('s', arr[2], color="#B82E2E")
        ax.barh('s', arr[0], left=arr[2], color="#7F7F7F")
        ax.barh('s', arr[1], left=arr[0]+arr[2], color="#3366CC")
        
        for c in ax.containers:
        
            # customize the label to account for cases when there might not be a bar section
            labels = [f'{w:.2f}%' if (w := v.get_width()) > 0 else '' for v in c ]
            
            # set the bar label
            ax.bar_label(c, labels=labels, label_type='center', fontsize=22, color='white')
        
        # ax.legend(loc='best', fontsize=25)
            
        fig.patch.set_visible(False)
        ax.axis('off')
        
        st.pyplot(fig)
        
    except:
        pass
## waffle chart

count_win = df_pick_colored.loc[df_pick_colored['result'] == 'win'].shape[0]

count_draw = df_pick_colored.loc[df_pick_colored['result'] == 'draw'].shape[0]

count_lose = df_pick_colored.loc[df_pick_colored['result'] == 'lose'].shape[0]

year_win = df_pick_colored.loc[df_pick_colored['result'] == 'win', 'date'].apply(lambda x: x.year)

year_draw = df_pick_colored.loc[df_pick_colored['result'] == 'draw', 'date'].apply(lambda x: x.year)

year_lose = df_pick_colored.loc[df_pick_colored['result'] == 'lose', 'date'].apply(lambda x: x.year)



move_win = df_pick_colored.loc[df_pick_colored['result'] == 'win', 'move'].astype('str')

move_draw = df_pick_colored.loc[df_pick_colored['result'] == 'draw', 'move'].astype('str')

move_lose = df_pick_colored.loc[df_pick_colored['result'] == 'lose', 'move'].astype('str')

site_win = df_pick_colored.loc[df_pick_colored['result'] == 'win', 'site']

site_draw = df_pick_colored.loc[df_pick_colored['result'] == 'draw', 'site']

site_lose = df_pick_colored.loc[df_pick_colored['result'] == 'lose', 'site']


rem_dic = {
    0:0,
    1:3,
    2:2,
    3:1,
}

count_empty = rem_dic[(count_win + count_draw + count_lose) % 4]

ar_win = np.full((count_win, 1), 3)
ar_draw = np.full((count_draw, 1), 2)
ar_lose = np.full((count_lose, 1), 1)
ar_empty = np.full((count_empty, 1), 0)

z = np.concatenate((ar_win, ar_draw, ar_lose, ar_empty))

z = np.reshape(z, (-1, 4)).transpose()

m = z.shape[0]
n = z.shape[1]


custom_data_empty = np.full((count_empty), '')

year_concat = np.concatenate((year_win, year_draw, year_lose, custom_data_empty)).reshape(n,m).transpose()

site_concat = np.concatenate((site_win, site_draw, site_lose, custom_data_empty)).reshape(n,m).transpose()

move_concat = np.concatenate((move_win, move_draw, move_lose, custom_data_empty)).reshape(n,m).transpose()


d = {3: f"{pick_name_left}",
    2: "Draw",
    1: f"{pick_name_right}",
    0:''}

M = max([len(s) for s in d.values()])

customdata= np.empty((m,n), dtype=f'<U{M}')

for i in range(m):
    for j in range(n):           
        customdata[i,j] = d[z[i, j]] 



#Normalizing the three possible z-values we get 1/3, 2/3, 1;
# define a discrete colorscale that maps 1/3, 2/3, 1 to distinct colors:

if count_empty == 0:
    

    if (count_lose == 0) & (count_draw == 0):
        colorscale = [[0, "#B82E2E"],
                    [0.33, "#B82E2E"],
                    [0.66, "#B82E2E"],
                    [1,  "#B82E2E"],
                    ]

    elif (count_lose == 0) & (count_win == 0):
        colorscale = [[0, "#7F7F7F"],
                    [0.33, "#7F7F7F"],
                    [0.66, "#7F7F7F"],
                    [1,  "#7F7F7F"],
                    ]
    
    elif (count_draw == 0) & (count_win == 0):
        colorscale = [[0, "#3366CC"],
                    [0.33, "#3366CC"],
                    [0.66, "#3366CC"],
                    [1,  "#3366CC"],
                    ]
    
    elif count_lose == 0:
        colorscale = [[0, "#7F7F7F"],
                    [0.33, "#7F7F7F"],
                    [0.66, "#B82E2E"],
                    [1,  "#B82E2E"],
                    ]

    elif count_draw == 0:
        colorscale = [[0, "#3366CC"],
                    [0.33, "#3366CC"],
                    [0.66, "#B82E2E"],
                    [1,  "#B82E2E"],
                    ]
        
    elif count_win == 0:
        colorscale = [[0, "#3366CC"],
                    [0.33, "#3366CC"],
                    [0.66, "#7F7F7F"],
                    [1,  "#7F7F7F"],
                    ]
        
    else :
        colorscale = [[0, "#3366CC"],
                    [0.33, "#7F7F7F"],
                    [0.66, "#7F7F7F"],
                    [1,  "#B82E2E"],
                    ]

    
    
else:
    if (count_lose == 0) & (count_draw == 0):
        colorscale = [[0, "#0e1117"],
                    [0.33, "#0e1117"],
                    [0.66, "#B82E2E"],
                    [1,  "#B82E2E"],
                    ]

    elif (count_lose == 0) & (count_win == 0):
        colorscale = [[0, "#0e1117"],
                    [0.33, "#0e1117"],
                    [0.66, "#7F7F7F"],
                    [1,  "#7F7F7F"],
                    ]
    
    elif (count_draw == 0) & (count_win == 0):
        colorscale = [[0, "#0e1117"],
                    [0.33, "#0e1117"],
                    [0.66, "#3366CC"],
                    [1,  "#3366CC"],
                    ]
    
    elif count_lose == 0:
        
        colorscale = [[0, "#0e1117"],
                    [0.33, "#7F7F7F"],
                    [0.66, "#7F7F7F"],
                    [1,  "#B82E2E"],
                    ]

    elif count_draw == 0:
        colorscale = [[0, "#0e1117"],
                    [0.33, "#3366CC"],
                    [0.66, "#3366CC"],
                    [1,  "#B82E2E"],
                    ]
        
    elif count_win == 0:
        colorscale = [[0, "#0e1117"],
                    [0.33, "#3366CC"],
                    [0.66, "#3366CC"],
                    [1,  "#7F7F7F"],
                    ]
    
    else :
        colorscale = [[0, "#0e1117"],
                    [0.33, "#3366CC"],
                    [0.66, "#7F7F7F"],
                    [1,  "#B82E2E"],
                    ]
fig = go.Figure(go.Heatmap(z=z, 
                           customdata=np.stack((customdata, move_concat, site_concat, year_concat), axis=-1), xgap=4, ygap=4,
                           colorscale=colorscale, showscale=False,
                           hovertemplate='<b>Winner</b>: %{customdata[0]}<br>' +
                                         '<b>Moves</b>: %{customdata[1]}<br>' +
                                         '<b>Site</b>: %{customdata[2]}<br>' +
                                         '<b>Year</b>: %{customdata[3]}' +
                                         '<extra></extra>',))


fig.update_layout(template='simple_white', margin_t=20, height=275)

fig.update_yaxes(showticklabels=False, ticks="", showgrid=False, autorange="reversed")

fig.update_xaxes(showticklabels=False, ticks="", showgrid=False)

st.plotly_chart(fig, theme="streamlit", use_container_width=True)