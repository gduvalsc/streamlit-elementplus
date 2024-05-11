import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Result", divider="rainbow")

col1, col2, col3, col4 = st.columns([1,1,1,1])
with col1:
    Result(title='Success tip', icon='success', description='Explanation about success', **theme)
with col2:
    Result(title='Info tip', icon='info', description='Explanation about info', **theme)
with col3:
    Result(title='Warning tip', icon='warning', description='Explanation about warning', **theme)
with col4:
    Result(title='Error tip', icon='error', description='Explanation about error', **theme)