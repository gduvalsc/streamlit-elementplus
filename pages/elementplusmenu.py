import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Menu", divider="rainbow")
item1 = dict(index="1", type="item", label="Option 1")
item2 = dict(index="2", type="item", label="Option 2")
item31 = dict(index="31", type="item", label= "Sub option 31")
item32 = dict(index="32", type="item", label= "Sub option 32")
item33 = dict(index="33", type="item", label= "Sub option 33", disabled=True)
item34 = dict(index="34", type="item", label= "Sub option 34")
item3 = dict(index="3", type="submenu", label="Option 3", items=[item31, item32, item33, item34])
item4 = dict(index="4", type="item", label="Disabled", disabled=True)
item5 = dict(index="5", type="item", label="Option 5")
item6 = dict(index="6", type="item", label="Option 6")
item7 = dict(index="7", type="item", label="Option 7")
item8 = dict(index="8", type="item", label="Option 8")
item9 = dict(index="9", type="item", label="Option 9")
x = Menu(items=[item1, item2, item3, item4, item5, item6, item7, item8, item9], default_active="1", ellipsis=True, default="1", mode="horizontal", **theme)
st.markdown(f"## Option {x.get()}")

