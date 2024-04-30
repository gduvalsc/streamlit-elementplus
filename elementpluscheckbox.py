import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Checkbox", divider="rainbow")
st.markdown("Element Plus offers 3 tags for working with checkboxes: '**el-checkbox**', '**el-checkbox-button**', and '**el-checkbox-group**'. The functionalities of 'el-checkbox' on its own do not offer any advantage compared to the standard '**st.checkbox**' element provided by Streamlit. However, the visual rendering of 'checkbox buttons' and the additional features of 'checkbox groups' are of additional interest.")
st.markdown("This '**checkbox**' section deals with traditional checkboxes encapsulated within a '**checkbox group**'. As for the '**checkbox buttons**' part, you should refer to the corresponding section. There are no differences between the two types; only the rendering is different.")
cb1 = dict(label='Option A', truevalue='Value true A', falsevalue='Value false A', selected=True, id='a')
cb2 = dict(label='Option B', truevalue='Value true B', falsevalue='Value false B', id='b')
cb3 = dict(label='Option C', truevalue='Value true C', falsevalue='Value false C', id='c')
cb4 = dict(label='Disabled', truevalue='Value true D', falsevalue='Value false D', disabled=True, id='d')
cb5 = dict(label='Selected and disabled', truevalue='Value true E', falsevalue='Value false E', disabled=True, selected=True, id='e')
checkb1 = [cb1, cb2, cb3, cb4, cb5]
defaultv = {x['id']:x['truevalue'] if 'selected' in x and x['selected'] else x['falsevalue'] for x in checkb1}
cbg1 = Checkbox(checkboxes=checkb1, size="large", default=defaultv)
with st.expander("Code"):
        st.code("""
        cb1 = dict(label='Option A', truevalue='Value true A', falsevalue='Value false A', selected=True, id='a')
        cb2 = dict(label='Option B', truevalue='Value true B', falsevalue='Value false B', id='b')
        cb3 = dict(label='Option C', truevalue='Value true C', falsevalue='Value false C', id='c')
        cb4 = dict(label='Disabled', truevalue='Value true D', falsevalue='Value false D', disabled=True, id='d')
        cb5 = dict(label='Selected and disabled', truevalue='Value true E', falsevalue='Value false E', disabled=True, selected=True, id='e')
        checkb1 = [cb1, cb2, cb3, cb4, cb5]
        defaultv = {x['id']:x['truevalue'] if 'selected' in x and x['selected'] else x['falsevalue'] for x in checkb1}
        cbg1 = Checkbox(checkboxes=checkb1, size="large", default=defaultv)
        """)
st.markdown("The value returned by this group of checkboxes is as follows:")
st.write(cbg1.get())
st.markdown("Each checkbox is identified by an '**id**'. In our example, the 'ids' are 'a', 'b', 'c', 'd', and 'e'. Each checkbox also has a '**label**' that will appear on the HTML page. The values returned by the checkbox must be defined at its level through the attributes '**truevalue**' and '**falsevalue**'. A checkbox can be pre-selected (attribute '**select**'). Finally, a checkbox can be disabled (attribute '**disabled**' and even disabled and pre-selected.")
st.markdown("Unlike buttons, which present issues with side effects in Streamlit, checkboxes pose far fewer problems. It is not necessary to reinstantiate them after each use of the widget because they contain all the necessary information to define the values returned to Python.")
st.markdown("The information returned to Python is a structure containing the identifier of the checkbox and the value selected by the user.")
st.markdown("###### Some examples of checkboxes:")
Checkbox(checkboxes=checkb1, key='cbg2', size="large", default=defaultv)
with st.expander("Code"):
        st.code("""
        Checkbox(checkboxes=checkb1, key='cbg2', size="large", default=defaultv)
        """)
Checkbox(checkboxes=checkb1, key='cbg3', size="small", default=defaultv)
with st.expander("Code"):
        st.code("""
        Checkbox(checkboxes=checkb1, key='cbg3', size="small", default=defaultv)
        """)
Checkbox(checkboxes=checkb1, key='cbg4', disabled=True, default=defaultv)
with st.expander("Code"):
        st.code("""
        Checkbox(checkboxes=checkb1, key='cbg4', disabled=True, default=defaultv)
        """)
cb1 = dict(label='Option A', truevalue='Value true A', falsevalue='Value false A', border=True, selected=True, id='a')
cb2 = dict(label='Option B', truevalue='Value true B', falsevalue='Value false B', border=True, id='b')
cb3 = dict(label='Option C', truevalue='Value true C', falsevalue='Value false C', id='c')
cb4 = dict(label='Disabled', truevalue='Value true D', falsevalue='Value false D', disabled=True, id='d')
cb5 = dict(label='Selected and disabled', truevalue='Value true E', falsevalue='Value false E', disabled=True, selected=True, id='e')
checkb1 = [cb1, cb2, cb3, cb4, cb5]
defaultv = {x['id']:x['truevalue'] if 'selected' in x and x['selected'] else x['falsevalue'] for x in checkb1}
cbg5 = Checkbox(checkboxes=checkb1, key='cbg5', size="large", default=defaultv)
with st.expander("Code"):
        st.code("""
        cb1 = dict(label='Option A', truevalue='Value true A', falsevalue='Value false A', border=True, selected=True, id='a')
        cb2 = dict(label='Option B', truevalue='Value true B', falsevalue='Value false B', border=True, id='b')
        cb3 = dict(label='Option C', truevalue='Value true C', falsevalue='Value false C', id='c')
        cb4 = dict(label='Disabled', truevalue='Value true D', falsevalue='Value false D', disabled=True, id='d')
        cb5 = dict(label='Selected and disabled', truevalue='Value true E', falsevalue='Value false E', disabled=True, selected=True, id='e')
        checkb1 = [cb1, cb2, cb3, cb4, cb5]
        defaultv = {x['id']:x['truevalue'] if 'selected' in x and x['selected'] else x['falsevalue'] for x in checkb1}
        cbg5 = Checkbox(checkboxes=checkb1, key='cbg5', size="large", default=defaultv)
        """)

