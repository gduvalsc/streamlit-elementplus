import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Progress", divider="rainbow")
Progress(percentage=30)
Progress(percentage=100, status="success")
Progress(percentage=50, status="warning")
Progress(percentage=5, status="exception")
Progress(percentage=40, stroke_width=25, text_inside=True)

color1 = dict(color='#f56c6c', percentage=20)
color2 = dict(color='#e6a23c', percentage=40)
color3 = dict(color='#5cb87a', percentage=60)
color4 = dict(color='#1989fa', percentage=80)
color5 = dict(color='#6f7ad3', percentage=100)
custcolor = [color1, color2, color3, color4, color5]

Progress(percentage=18, stroke_width=25, text_inside=True, color=custcolor, striped=True, striped_flow=True, duration=1)
Progress(percentage=22, stroke_width=25, text_inside=True, color=custcolor, striped=True, striped_flow=True, duration=1)
Progress(percentage=43, stroke_width=25, text_inside=True, color=custcolor, striped=True, striped_flow=True, duration=1)
Progress(percentage=67, stroke_width=25, text_inside=True, color=custcolor, striped=True, striped_flow=True, duration=1)
Progress(percentage=92, stroke_width=25, text_inside=True, color=custcolor, striped=True, striped_flow=True, duration=1)


Progress(percentage=92, stroke_width=15, color=custcolor, striped=True, striped_flow=True, duration=10, type='dashboard')
Progress(percentage=43, stroke_width=15, color=custcolor, striped=True, striped_flow=True, duration=10, type='circle')


Progress(percentage=50, indeterminate=True, stroke_width=14, text_inside=True, duration=10)