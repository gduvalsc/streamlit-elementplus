import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Slider", divider="rainbow")

Slider(label='Default value', labelwidth=5, sliderwidth=15, **theme)  
Slider(label='Initial value', value=46, labelwidth=5, sliderwidth=15, **theme)
Slider(label='Disabled', value=30, disabled=True, labelwidth=5, sliderwidth=15, **theme)  
Slider(label='Custom steps', value=20, step=10, labelwidth=5, sliderwidth=15, **theme)  
Slider(label='Show input', value=10, step=10, show_input=True, labelwidth=5, sliderwidth=15, **theme)  
Slider(label='Range selection', value=[10,50], step=10, range=True, labelwidth=5, sliderwidth=15, **theme)  