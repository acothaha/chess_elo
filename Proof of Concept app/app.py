import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
from affinda import AffindaAPI, TokenCredential
from io import StringIO

token = "b788ee6044809ec4c425ec29f08a1f5f79f6b516"

credential = TokenCredential(token=token)
client = AffindaAPI(credential=credential)

# automatically hide sidebar and removing its value,
st.set_page_config(initial_sidebar_state="collapsed", page_icon="🧊")
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

# main title
st.write("# CV Parsing Demo")

# upload widget
cv = st.file_uploader('Upload your CV/Resume', type=['pdf', 'docx'], label_visibility='hidden')

# define a session state for storing the result of parsing
if 'parsed_cv' not in st.session_state:
	st.session_state.parsed_cv = 0


if cv:
    # st.text(cv.read())
    base64_pdf = base64.b64encode(cv.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'

    st.markdown(pdf_display, unsafe_allow_html=True)
    
    # st.markdown('<a href="/next_page" target="_self">Next page</a>', unsafe_allow_html=True)

    # assign the parsed_cv into a session state
    st.session_state.parsed_cv = base64_pdf

    submit = st.button("Submit")
    if submit:      
        with st.spinner(text='In progress'):
            # with open(cv, "r") as pdf:
            # input = StringIO(cv.getvalue().decode("utf-8"))
            resume = client.create_resume(file=base64_pdf)
            st.session_state.parsed_cv = resume

            # test = data_cv('test yoooo')
            switch_page('page 1')
        # st.markdown(parsed_cv.as_dict())

