import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
from io import StringIO
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide", 
    page_title="testff gan", 
    )
# CSS style
st.markdown('''
<style>
.first_title {
    font-family: Georgia, serif;
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
</style>
''', unsafe_allow_html=True)




st.markdown('''
    <div class="first_title">
        Markdown css styles
    </div>
    ''', unsafe_allow_html=True)


c1, c2 = st.columns((3, 2))
with c2:
    st.write("##")
    st.write("##")
    st.markdown("hilih kindsfgsdfredsvnuhviufhviuhduvhaeiurhvidshvihfduhvifhvuidhfsvihuierhvudsbvuab")
st.write("##")
with c1:
    st.write("##")
    st.write("##")
    st.markdown(
        '<p class="intro">Bienvenue sur la <b>no-code AI platform</b> ! Déposez vos datasets csv ou excel ou choisissez en un parmi ceux proposés et commencez votre analyse dès maintenant ! Cherchez les variables les plus intéressantes, visualisez vos données, et créez vos modèles de Machine Learning en toute simplicité.' +
        ' Si vous choisissez de travailler avec votre dataset et que vous voulez effectuez des modifications sur celui-ci, il faudra le télécharger une fois les modifications faites pour pouvoir l\'utiliser sur les autres pages. </p>',
        unsafe_allow_html=True)
    st.markdown(
        '<p class="intro">Un tutoriel sur l\'utilisation de ce site est disponible sur le repo Github. En cas de bug ou d\'erreur veuillez m\'en informer par mail ou sur Discord.</p>',
        unsafe_allow_html=True)
    st.markdown(
        '<p class="intro"><b>Commencez par choisir un dataset dans la section Dataset !</b></p>',
        unsafe_allow_html=True)



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
        name,
        opening_moves,
        year,
        rn
    FROM 
        `esoteric-code-377203.chess_elo_production.chess_elo_top`
    ORDER BY 
        ranking, rn
    """

df = client.query(sql).to_dataframe()

name = df['player_name'].unique()




pick_name = st.selectbox('Pick one', name)

df_pick = df.loc[df['player_name'] == pick_name].reset_index(drop=True)
st.dataframe(df_pick)
fig, ax = plt.subplots()
ax.plot(df_pick['rating'])

st.pyplot(fig)

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

