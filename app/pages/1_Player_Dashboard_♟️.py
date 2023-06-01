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
    page_title="Player Dashboard",
    page_icon="♟️",
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


st.markdown('''
    <div class="first_title">
       ♟️ Player Dashboard
    </div>
    ''', unsafe_allow_html=True)


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

pick_name = st.sidebar.selectbox('Choose a Player', name)

c_name, c_choose = st.columns((10,2))


with c_name:

    st.markdown(f'''
        # {pick_name}
        ''', unsafe_allow_html=True)

bio_pick = bio_content[pick_name]

c11, c12, c13, c14, c15 = st.columns((0.5, 0.4, 1, 0.25, 0.5))


with c11:
    st.text('')
    st.markdown(
    f"""
    <div style="text-align: left;"><img src={bio_pick['image']} width="250" alt="My Image" /></div>
    """, unsafe_allow_html=True
    )

with c12:
    st.text('')

    st.markdown(f'<p class="dashboard_title">Title</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="dashboard_title">Born</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="dashboard_title">Live Rating</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="dashboard_title">FIDE Rating</p>', unsafe_allow_html=True)


with c13:
    st.text('')

    st.markdown(f'<p class="intro">{bio_pick["title"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="intro">{bio_pick["born"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="intro">{bio_pick["live_rating"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="intro">{bio_pick["FIDE_rating"]}</p>', unsafe_allow_html=True)
 
with c14:
    st.text('')

    st.markdown(f'<p class="dashboard_title">World</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="dashboard_title">FIDE Peak</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="dashboard_title">Rapid</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="dashboard_title">Blitz</p>', unsafe_allow_html=True)

with c15:
    st.text('')

    st.markdown(f'<p class="intro">{bio_pick["world"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="intro">{bio_pick["FIDE_peak"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="intro">{bio_pick["rapid"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="intro">{bio_pick["blitz"]}</p>', unsafe_allow_html=True)

c22, c21 = st.columns((1, 4))

df_pick = df.loc[df['player_name'] == pick_name].reset_index(drop=True)

with c21:
    

    c210, c211, c212, c213, c214 = st.columns((1.1,1,0.1,1,1))

    with c211:

        start = st.date_input(
                    'start date',
                    value=df_pick['date'].min(),
                    min_value=df_pick['date'].min(),
                    max_value=df_pick['date'].max(),
                    label_visibility='hidden' )
    
    with c212:
        st.markdown(f'# -', unsafe_allow_html=True)

    with c213:
        end = st.date_input(
                    'end date',
                    value=df_pick['date'].max(),
                    min_value=df_pick['date'].min(),
                    max_value=df_pick['date'].max(),
                    label_visibility='hidden')

    # ax.plot(df_pick.loc[df_pick['year'].isin(year_plot_choose), 'rating'])
    # ax.invert_xaxis()
    # st.pyplot(fig)

    df_line = df_pick.loc[(df['date'] >= start) & (df['date'] <= end)]
    df_line = df_line.groupby(['date'])['rating'].mean().reset_index()

    fig = px.line(df_line, x="date", y="rating", markers=True)
    fig.update_layout(autosize=True, title=dict(text=f"ELO Overtime", automargin=True))
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, )

with c22:

    color = st.select_slider(
    'Select a color of the rainbow',
    options=['⚪White', 'All', '⚫Black'], value='All', label_visibility='hidden')

    if color == 'All':
        df_pie = df_pick.loc[(df['date'] >= start) & (df['date'] <= end), 'result'].value_counts()
    elif color == '⚪White':
        df_pie = df_pick.loc[(df['date'] >= start) & (df['date'] <= end) & (df['play_as'] == 'white'), 'result'].value_counts()
    else:
        df_pie = df_pick.loc[(df['date'] >= start) & (df['date'] <= end) & (df['play_as'] == 'black'), 'result'].value_counts()
    

    fig = px.pie(df_pie, values="count", names=df_pie.index, color=df_pie.index,
                color_discrete_map={'win':'#B82E2E',
                                    'lose':'#3366CC',
                                    'draw':'#7F7F7F'
                                    })
    fig.update(layout_showlegend=False)
    fig.update_layout(width=400, height=400, autosize=True, title=dict(text=f"Result % ({color})", automargin=True, y=0.9))
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.markdown('###### **Last 10 matches**')
st.dataframe(df_pick[['date', 'site' ,'player_name', 'play_as', 'opponent', 'move', 'result']][:10]. \
             style.applymap(lambda x: 'background-color : #B82E2E' if x == 'win' else \
                            'background-color : #3366CC' if x == 'lose' else \
                            'background-color : #7F7F7F', subset=['result']), use_container_width=True)

# token = "b788ee6044809ec4c425ec29f08a1f5f79f6b516"

# credential = TokenCredential(token=token)
# client = AffindaAPI(credential=credential)

# # automatically hide sidebar and removing its value,
# st.set_page_config(initial_sidebar_state="collapsed", page_icon="🧊")
# st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

# # main title
# st.write("# CV Parsing Demo")

# # upload widget
# cv = st.file_uploader('Upload your CV/Resume', type=['pdf', 'docx'], label_visibility='hidden')

# # define a session state for storing the result of parsing
# if 'parsed_cv' not in st.session_state:
# 	st.session_state.parsed_cv = 0


# if cv:
#     # st.text(cv.read())
#     base64_pdf = base64.b64encode(cv.read()).decode('utf-8')
#     pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'

#     st.markdown(pdf_display, unsafe_allow_html=True)
    
#     # st.markdown('<a href="/next_page" target="_self">Next page</a>', unsafe_allow_html=True)

#     # assign the parsed_cv into a session state
#     st.session_state.parsed_cv = base64_pdf

#     submit = st.button("Submit")
#     if submit:      
#         with st.spinner(text='In progress'):
#             # with open(cv, "r") as pdf:
#             # input = StringIO(cv.getvalue().decode("utf-8"))
#             resume = client.create_resume(file=base64_pdf)
#             st.session_state.parsed_cv = resume

#             # test = data_cv('test yoooo')
#             switch_page('page 1')
#         # st.markdown(parsed_cv.as_dict())

