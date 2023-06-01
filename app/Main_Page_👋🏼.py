import streamlit as st


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


st.write("# Welcome to  👋")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

