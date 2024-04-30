import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Tag", divider="rainbow")

tag1 = dict(name='Tag 1', type='primary')
tag2 = dict(name='Tag 2', type='success')
tag3 = dict(name='Tag 3', type='info')
tag4 = dict(name='Tag 4', type='warning')
tag5 = dict(name='Tag 5', type='danger')
tags1 = [tag1, tag2, tag3, tag4, tag5]
defaultv = [x['name'] for x in tags1]
t1 = Tag(tags=tags1, label='Tags', size='large', effect='dark', round=True, editable=True, default=defaultv)
st.write(t1.get())