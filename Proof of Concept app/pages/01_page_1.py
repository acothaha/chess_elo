import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
import datetime
import time

# with st.spinner(text='In progress'):
#    time.sleep(5)
#    st.success('Done')

st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

if 'parsed_cv' not in st.session_state:
	st.session_state.parsed_cv = 0

resume = st.session_state.parsed_cv.as_dict()

col1, col2 = st.columns(2)

st.markdown('## Basic Information')

def text_process(text):
    return text.lower().title()

val_full_name = text_process(resume['data']['name']['raw'])
full_name = st.text_input('Full Name', value=val_full_name)

val_location = text_process(resume['data']['location']['formatted'])
location = st.text_input('Location', value=val_location)

col1_basic, col2_basic = st.columns(2)

val_email = resume['data']['emails'][0]
email = col1_basic.text_input('Email', value=val_email)

val_phone = resume['data']['phone_numbers'][0]
full_name = col2_basic.text_input('Phone Number', value=val_phone)

try:
    val_linkedin = resume['data']['linkedin']

except:
    val_linkedin = ''

linkedin = col1_basic.text_input('Linkedin', value=val_linkedin)

try:
    
    val_website = resume['data']['websites'][0]
    if linkedin == val_website:
        val_website = resume['data']['websites'][1]
except:
    val_website = ''

website = col2_basic.text_input('Website', value=val_website)

st.markdown('## Work Experiences')

experiences = resume['data']['work_experience']
lst_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
for n, exp in enumerate(experiences):
    st.markdown(f'#### Work Experience {n+1}')

    try:

        val_company = exp['organization']
        company = st.text_input('Company', value=val_company, key=f'exp_company_{n}')

    except:
        val_company = ''
        company = st.text_input('Company', value=val_company, key=f'exp_company_{n}')

    try:
        val_job_title = exp['job_title']
        job_title = st.text_input('Job Title', value=val_job_title, key=f'exp_job_title_{n}')

    except:
        val_job_title = ''
        job_title = st.text_input('Job Title', value=val_job_title, key=f'exp_job_title_{n}')

    col1_exp, col2_exp = st.columns(2)

    try:
        val_exp_date_start_month = int(exp['dates']['start_date'].split('-')[1])
        val_exp_date_start_year = exp['dates']['start_date'].split('-')[0]
        date_exp_start_month = col1_exp.selectbox('Start Date', lst_months, key = 'exp_date_start_month' + str(n), index=val_exp_date_start_month-1)
        date_exp_start_year = col2_exp.text_input('', value=val_exp_date_start_year, key = 'exp_date_start_year' + str(n))
    except:
        date_exp_start_month = col1_exp.selectbox('Start Date', lst_months, key = 'exp_date_start_month' + str(n), index=0)
        date_exp_start_year = col2_exp.text_input('', value='', key = 'exp_date_start_year' + str(n))

    try:
        val_exp_date_end_month = int(exp['dates']['end_date'].split('-')[1])
        val_exp_date_end_year = exp['dates']['end_date'].split('-')[0]
        date_exp_end_month = col1_exp.selectbox('Start Date', lst_months, key='exp_date_end_month' + str(n), index=val_exp_date_end_month-1)
        date_exp_end_year = col2_exp.text_input('', value=val_exp_date_end_year, key='exp_date_end_year' + str(n))
    except:
        date_exp_start_month = col1_exp.selectbox('Start Date', lst_months, key = 'exp_date_end_month' + str(n), index=0)
        date_exp_start_year = col2_exp.text_input('', value='', key = 'exp_date_end_year' + str(n))


st.markdown('## Skills')

col_skill = st.columns(3)

n_col_skill = 0
n_key_skill = 0
skill_dict = resume['data']['skills']

for skill in skill_dict:

    placeholder = col_skill[n_col_skill].empty()
    isclick = placeholder.checkbox(skill['name'], value=True, key=f'skill_{n_key_skill}')
    if isclick == False:
        placeholder.empty()
    n_key_skill += 1
    n_col_skill += 1
    if n_col_skill == 3:
        n_col_skill = 0


st.markdown('## Languages')

col_lang = st.columns(3)

n_col_lang = 0
n_key_lang = 0
lang_dict = resume['data']['languages']

for lang in lang_dict:

    placeholder = col_lang[n_col_lang].empty()
    isclick = placeholder.checkbox(lang, value=True, key=f'lang_{n_key_lang}')
    if isclick == False:
        placeholder.empty()
    n_key_lang += 1
    n_col_lang += 1
    if n_col_lang == 3:
        n_col_lang = 0


st.markdown('## Educations')

educations = resume['data']['education']
for n, edu in enumerate(educations):
    st.markdown(f'#### Education {n+1}')
    try:

        val_institution = edu['organization']
        institution = st.text_input('Institution', value=val_institution, key=f'edu_institution_{n}')

    except:
        val_institution = ''
        institution = st.text_input('Institution', value=val_institution, key=f'edu_institution_{n}')
    
    try:
        val_edu_level = edu['accreditation']['education_level']
        edu_level = st.text_input('Education Level', value=val_edu_level, key=f'edu_level_{n}')
    except:
        val_edu_level = ''
        edu_level = st.text_input('Education Level', value=val_edu_level, key=f'edu_level_{n}')

    val_major = edu['accreditation']['education']
    major = st.text_input('Major', value=val_major, key=f'edu_major_{n}')

    col1_edu, col2_edu = st.columns(2)

    try:
        val_edu_date_start_month = int(edu['dates']['start_date'].split('-')[1])
        val_edu_date_start_year = edu['dates']['start_date'].split('-')[0]
        date_edu_start_month = col1_edu.selectbox('Start Date', lst_months, key = 'edu_date_start_month' + str(n), index=val_edu_date_start_month-1)
        date_edu_start_year = col2_edu.text_input('', value=val_edu_date_start_year, key = 'edu_date_start_year' + str(n))
    except:
        date_edu_start_month = col1_edu.selectbox('Start Date', lst_months, key = 'edu_date_start_month' + str(n), index=0)
        date_edu_start_year = col2_edu.text_input('', value='', key = 'edu_date_start_year' + str(n))

    try:
        val_edu_date_end_month = int(edu['dates']['completion_date'].split('-')[1])
        val_edu_date_end_year = edu['dates']['completion_date'].split('-')[0]
        date_edu_end_month = col1_edu.selectbox('Completion Date', lst_months, key='edu_date_end_month' + str(n), index=val_edu_date_end_month-1)
        date_edu_end_year = col2_edu.text_input('', value=val_edu_date_end_year, key='edu_date_end_year' + str(n))
    except:
        date_edu_start_month = col1_edu.selectbox('Completion date', lst_months, key = 'edu_date_end_month' + str(n), index=0)
        date_edu_start_year = col2_edu.text_input('', value='', key = 'edu_date_end_year' + str(n))
        

resume


# experiences = resume['data']['work_experience']
# lst_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# for n, exp in enumerate(experiences):
#     st.markdown(f'#### Work Experience {n+1}')

#     val_company = exp['organization']
#     company = st.text_input('Company', value=val_company)

#     val_job_title = exp['job_title']
#     job_title = st.text_input('Job Title', value=val_job_title)

#     col1_exp, col2_exp = st.columns(2)

#     try:
#         val_date_start_month = int(exp['dates']['start_date'].split('-')[1])
#         val_date_start_year = exp['dates']['start_date'].split('-')[0]
#         date_start_month = col1_exp.selectbox('Start Date', lst_months, key = 'date_start_month' + str(n), index=val_date_start_month-1)
#         date_start_year = col2_exp.text_input('', value=val_date_start_year, key = 'date_start_year' + str(n))
#     except:
#         date_start_month = col1_exp.selectbox('Start Date', lst_months, key = 'date_start_month' + str(n), index=0)
#         date_start_year = col2_exp.text_input('', value='', key = 'date_start_year' + str(n))

#     try:
#         val_date_end_month = int(exp['dates']['end_date'].split('-')[1])
#         val_date_end_year = exp['dates']['end_date'].split('-')[0]
#         date_end_month = col1_exp.selectbox('Start Date', lst_months, key='date_end_month' + str(n), index=val_date_end_month-1)
#         date_end_year = col2_exp.text_input('', value=val_date_end_year, key='date_end_year' + str(n))
#     except:
#         date_start_month = col1_exp.selectbox('Start Date', lst_months, key = 'date_end_month' + str(n), index=0)
        # date_start_year = col2_exp.text_input('', value='', key = 'date_end_year' + str(n))

    
    
# val_full_name = text_process(resume['data']['name']['raw'])
# full_name = st.text_input('Full Name', value=val_full_name)

# val_full_name = text_process(resume['data']['name']['raw'])
# full_name = st.text_input('Full Name', value=val_full_name)

# val_full_name = text_process(resume['data']['name']['raw'])
# full_name = st.text_input('Full Name', value=val_full_name)

# val_full_name = text_process(resume['data']['name']['raw'])
# full_name = st.text_input('Full Name', value=val_full_name)

# val_full_name = text_process(resume['data']['name']['raw'])
# full_name = st.text_input('Full Name', value=val_full_name)

# val_full_name = text_process(resume['data']['name']['raw'])
# full_name = st.text_input('Full Name', value=val_full_name)

# val_full_name = text_process(resume['data']['name']['raw'])
# full_name = st.text_input('Full Name', value=val_full_name)


# if show_pdf:
#     # base64_pdf = st.session_state.parsed_cv
#     # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
#     parsed_cv = st.session_state.parsed_cv
#     st.markdown(parsed_cv.as_dict(), unsafe_allow_html=True)
#     # test = st.session_state.count
#     # st.text(test)