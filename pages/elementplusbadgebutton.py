import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Badge button", divider="rainbow")

col1, col2, col3, col4,col5 = st.columns([1,1,1,1,1])
with col1:
    BadgeButton(label='Comments', badge_value=12, **theme)
with col2:
    BadgeButton(label='Replies', badge_value=5, badge_type='info', **theme)
with col3:
    BadgeButton(label='Comments', badge_value=1, badge_type='primary', **theme)
with col4:
    BadgeButton(label='Replies', badge_value=2, badge_type='warning', **theme)
with col5:
    BadgeButton(label='Custom', badge_value=1, badge_color='green', **theme)

col1, col2, col3, col4,col5 = st.columns([1,1,1,1,1])
with col1:
    BadgeButton(label='Comments', badge_value=110, badge_max=99, **theme)
with col2:
    BadgeButton(label='Replies', badge_value=15, badge_max=10, **theme)


col1, col2, col3, col4,col5 = st.columns([1,1,1,1,1])
with col1:
    BadgeButton(label='Comments', badge_value='new', **theme)
with col2:
    BadgeButton(label='Replies', badge_value='hot', **theme)

BadgeButton(icon='Share', badge_is_dot=True)


col1, col2, col3, col4,col5 = st.columns([1,1,1,1,1])
with col1:
    BadgeButton(label='Comments', badge_value=0, badge_show_zero=False, **theme)
with col2:
    BadgeButton(label='Comments', badge_value=0, badge_show_zero=True, **theme)

col1, col2, col3, col4,col5 = st.columns([1,1,1,1,1])
with col1:
    BadgeButton(label='Comments', badge_value=5, badge_hidden=False, **theme)
with col2:
    BadgeButton(label='Comments', badge_value=5, badge_hidden=True, **theme)
