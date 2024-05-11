import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Switch", divider="rainbow")

x = Switch(value=False, active_action_icon='Show', width=100, style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949")
st.write(x.get())