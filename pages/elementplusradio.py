import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Radio", divider="rainbow")
st.markdown("There is a standard function '**st.radio**' in Streamlit. In Element Plus, we have three HTML elements that handle the radio function: '**el-radio**', '**el-radio-group**', and '**el-radio-button**'. In Element Plus, the presentation differs from that of st.radio, so it's this aspect that makes Element Plus implementation interesting.")
st.markdown("This '**radio**' section deals with traditional radio butttons encapsulated within a '**radio group**'. As for the '**radio buttons**' part, you should refer to the corresponding section. There are no differences between the two types; only the rendering is different.")
rb1 = dict(label='New York', value='New York', selected=True)
rb2 = dict(label='Washington', value='Washington')
rb3 = dict(label='Los Angeles', value='Los Angeles')
rb4 = dict(label='Chicago', value='Chicago', disabled=True)
radio1 = [rb1, rb2, rb3, rb4]
defaultv = [x['value'] if 'selected' in x and x['selected'] else None for x in radio1][0]
ra1 = Radio(buttons=radio1, size="large", default=defaultv)
with st.expander("Code"):
        st.code("""
        rb1 = dict(label='New York', value='New York', selected=True)
        rb2 = dict(label='Washington', value='Washington')
        rb3 = dict(label='Los Angeles', value='Los Angeles')
        rb4 = dict(label='Chicago', value='Chicago', disabled=True)
        radio1 = [rb1, rb2, rb3, rb4]
        defaultv = [x['value'] if 'selected' in x and x['selected'] else None for x in radio1][0]
        ra1 = Radio(buttons=radio1, size="large", default=defaultv)
        """)
st.markdown("The value returned by this group of checkboxes is as follows:")
st.code(f'Returned value ===>  :             {ra1.get()}')
st.markdown("###### Some examples of radio buttons:")
ra2 = Radio(buttons=radio1, key="ra2", size="large", default=defaultv)
with st.expander("Code"):
        st.code("""
        ra2 = Radio(buttons=radio1, key="ra2", size="large", default=defaultv)
        """)
ra3 = Radio(buttons=radio1, key="ra3", size="small", default=defaultv)
with st.expander("Code"):
        st.code("""
        ra3 = Radio(buttons=radio1, key="ra3", size="small", default=defaultv)
        """)
ra4 = Radio(buttons=radio1, key="ra4", size="large", disabled=True, default=defaultv)
with st.expander("Code"):
        st.code("""
        ra4 = Radio(buttons=radio1, key="ra4", size="large", disabled=True, default=defaultv)
        """)