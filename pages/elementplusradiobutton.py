import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Radio button", divider="rainbow")
rb1 = dict(label='New York', value='New York', selected=True)
rb2 = dict(label='Washington', value='Washington')
rb3 = dict(label='Los Angeles', value='Los Angeles')
rb4 = dict(label='Chicago', value='Chicago', disabled=True)
radio1 = [rb1, rb2, rb3, rb4]
defaultv = [x['value'] if 'selected' in x and x['selected'] else None for x in radio1][0]
ra1 = RadioButton(buttons=radio1, size="large", default=defaultv)
with st.expander("Code"):
        st.code("""
        rb1 = dict(label='New York', value='New York', selected=True)
        rb2 = dict(label='Washington', value='Washington')
        rb3 = dict(label='Los Angeles', value='Los Angeles')
        rb4 = dict(label='Chicago', value='Chicago', disabled=True)
        radio1 = [rb1, rb2, rb3, rb4]
        defaultv = [x['value'] if 'selected' in x and x['selected'] else None for x in radio1][0]
        ra1 = RadioButton(buttons=radio1, size="large", default=defaultv)
        """)
st.markdown("The value returned by this group of checkboxes is as follows:")
st.code(f'Returned value ===>  :             {ra1.get()}')
st.markdown("###### Some examples of radio buttons:")
ra2 = RadioButton(buttons=radio1, key="ra2", size="large", default=defaultv)
with st.expander("Code"):
        st.code("""
        ra2 = RadioButton(buttons=radio1, key="ra2", size="large", default=defaultv)
        """)
ra2 = RadioButton(buttons=radio1, key="rax2", size="default", default=defaultv)
with st.expander("Code"):
        st.code("""
        ra2 = RadioButton(buttons=radio1, key="rax2", size="default", default=defaultv)
        """)
ra3 = RadioButton(buttons=radio1, key="ra3", size="small", default=defaultv)
with st.expander("Code"):
        st.code("""
        ra3 = RadioButton(buttons=radio1, key="ra3", size="small", default=defaultv)
        """)
ra4 = RadioButton(buttons=radio1, key="ra4", size="large", fill="yellow", disabled=True, default=defaultv)
with st.expander("Code"):
        st.code("""
        ra4 = RadioButton(buttons=radio1, key="ra4", size="large", fill="yellow", disabled=True, default=defaultv)
        """)
ra5 = RadioButton(buttons=radio1, key="ra5", size="large", fill="red", default=defaultv)
with st.expander("Code"):
        st.code("""
        ra5 = RadioButton(buttons=radio1, key="ra5", size="large", fill="red", default=defaultv)
        """)
ra6 = RadioButton(buttons=radio1, key="ra6", size="large", fill="lightgreen", textcolor="red", default=defaultv)
with st.expander("Code"):
        st.code("""
        ra6 = RadioButton(buttons=radio1, key="ra6", size="large", fill="lightgreen", textcolor="red", default=defaultv)
        """)