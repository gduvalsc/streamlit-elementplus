import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Tree", divider="rainbow")

data = """
- label: Level one 1
  id: 1
  _class: folder
  children:
    - label: Level two 1-1
      id: 1-1
      children:
        - label: Level three 1-1-1
          _class: leaf
          id: 1-1-1
- label: Level one 2
  id: 2
  _class: folder
  children:
    - label: Level two 2-1
      id: 2-1
      children:
        - label: Level three 2-1-1
          _class: leaf
          id: 2-1-1
    - label: Level two 2-2
      id: 2-2
      children:
        - label: Level three 2-2-1
          _class: leaf
          id: 2-2-1
- label: Level one 3
  id: 3
  _class: folder
  children:
    - label: Level two 3-1
      id: 3-1
      children:
        - label: Level three 3-1-1
          _class: leaf
          id: 3-1-1
    - label: Level two 3-2
      id: 3-2
      children:
        - label: Level three 3-2-1
          _class: leaf
          id: 3-2-1
"""
style='.folder svg {background-color:yellow} .folder span {color:red} .leaf span {color:blue}'

x = Tree(data=yaml.safe_load(data), accordion=False, expand_on_click_node=False, indent=50, draggable=True, icon="Folder", style=style, **theme)
st.write(x.get())


