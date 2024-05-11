import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Tree select", divider="rainbow")

data = """
- label: Level one 1
  value: 1
  children:
    - label: Level two 1-1
      value: 1-1
      children:
        - label: Level three 1-1-1
          value: 1-1-1
- label: Level one 2
  value: 2
  children:
    - label: Level two 2-1
      value: 2-1
      children:
        - label: Level three 2-1-1
          value: 2-1-1
    - label: Level two 2-2
      value: 2-2
      children:
        - label: Level three 2-2-1
          value: 2-2-1
- label: Level one 3
  value: 3
  children:
    - label: Level two 3-1
      value: 3-1
      children:
        - label: Level three 3-1-1
          value: 3-1-1
    - label: Level two 3-2
      value: 3-2
      children:
        - label: Level three 3-2-1
          value: 3-2-1
"""

x = TreeSelect(data=yaml.safe_load(data), placeholder='Select something', filterable=True, accordion=True, **theme)
st.write(x.get())