import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Checkbox button", divider="rainbow")
st.markdown("A button-style checkbox is used in the same way as a standard checkbox. Only the visual rendering is different.")
cb1 = dict(label='Option A', truevalue='Value true A', falsevalue='Value false A', selected=True, id='a')
cb2 = dict(label='Option B', truevalue='Value true B', falsevalue='Value false B', id='b')
cb3 = dict(label='Option C', truevalue='Value true C', falsevalue='Value false C', id='c')
cb4 = dict(label='Disabled', truevalue='Value true D', falsevalue='Value false D', disabled=True, id='d')
cb5 = dict(label='Selected and disabled', truevalue='Value true E', falsevalue='Value false E', disabled=True, selected=True, id='e')
checkb1 = [cb1, cb2, cb3, cb4, cb5]
defaultv = {x['id']:x['truevalue'] if 'selected' in x and x['selected'] else x['falsevalue'] for x in checkb1}
cbg1 = CheckboxButton(checkboxes=checkb1, size="large", default=defaultv)
with st.expander("Code"):
        st.code("""
        cb1 = dict(label='Option A', truevalue='Value true A', falsevalue='Value false A', selected=True, id='a')
        cb2 = dict(label='Option B', truevalue='Value true B', falsevalue='Value false B', id='b')
        cb3 = dict(label='Option C', truevalue='Value true C', falsevalue='Value false C', id='c')
        cb4 = dict(label='Disabled', truevalue='Value true D', falsevalue='Value false D', disabled=True, id='d')
        cb5 = dict(label='Selected and disabled', truevalue='Value true E', falsevalue='Value false E', disabled=True, selected=True, id='e')
        checkb1 = [cb1, cb2, cb3, cb4, cb5]
        defaultv = {x['id']:x['truevalue'] if 'selected' in x and x['selected'] else x['falsevalue'] for x in checkb1}
        cbg1 = CheckboxButton(checkboxes=checkb1, size="large", default=defaultv)
        """)
st.markdown("The value returned by this group of checkboxes is as follows:")
st.write(cbg1.get())
st.markdown("###### Some examples of checkboxes:")
CheckboxButton(checkboxes=checkb1, key='cbg2', size="large", default=defaultv)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg2', size="large", default=defaultv)
        """)
CheckboxButton(checkboxes=checkb1, key='cbg3', size="small", default=defaultv)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg3', size="small", default=defaultv)
        """)
CheckboxButton(checkboxes=checkb1, key='cbg4', disabled=True, default=defaultv)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg4', disabled=True, default=defaultv)
        """)
CheckboxButton(checkboxes=checkb1, key='cbg5', fill="red", default=defaultv)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg5', fill="red", default=defaultv)
        """)
CheckboxButton(checkboxes=checkb1, key='cbg6', fill="lightgreen", textcolor="red", default=defaultv)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg6', fill="lightgreen", textcolor="red", default=defaultv)
        """)
