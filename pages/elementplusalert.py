import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Alert", divider="rainbow")
st.markdown("###### Basic usage")
Alert(title="Success alert", type="success", **theme)
Alert(title="Info alert", type="info", **theme)
Alert(title="Warning alert", type="warning", **theme)
Alert(title="Error alert", type="error", **theme)
with st.expander("Code"):
        st.code("""
        Alert(title="Success alert", type="success", **theme)
        Alert(title="Info alert", type="info", **theme)
        Alert(title="Warning alert", type="warning", **theme)
        Alert(title="Error alert", type="error", **theme)
        """)

st.markdown("###### Theme")
Alert(title="Success alert", type="success", effect='dark', **theme)
Alert(title="Info alert", type="info", effect='dark', **theme)
Alert(title="Warning alert", type="warning", effect='dark', **theme)
Alert(title="Error alert", type="error", effect='dark', **theme)
with st.expander("Code"):
        st.code("""
        Alert(title="Success alert", type="success", effect='dark', **theme)
        Alert(title="Info alert", type="info", effect='dark', **theme)
        Alert(title="Warning alert", type="warning", effect='dark', **theme)
        Alert(title="Error alert", type="error", effect='dark', **theme)
        """)

st.markdown("###### Unclosable alert")
Alert(title="Unclosable error alert", type="error", effect='dark', closable=False)
with st.expander("Code"):
        st.code("""
        Alert(title="Unclosable error alert", type="error", effect='dark', closable=False)
        """)

st.markdown("###### With icon")
Alert(title="Success alert", type="success", show_icon=True, **theme)
Alert(title="Info alert", type="info", show_icon=True, **theme)
Alert(title="Warning alert", type="warning", show_icon=True, **theme)
Alert(title="Error alert", type="error", show_icon=True, **theme)
with st.expander("Code"):
        st.code("""
        Alert(title="Success alert", type="success", show_icon=True, **theme)
        Alert(title="Info alert", type="info", show_icon=True, **theme)
        Alert(title="Warning alert", type="warning", show_icon=True, **theme)
        Alert(title="Error alert", type="error", show_icon=True, **theme)
        """)
st.markdown("###### With icon and description")
Alert(title="Success alert", type="success", show_icon=True, description='This is an explanation', **theme)
Alert(title="Info alert", type="info", show_icon=True, description='This is an explanation', **theme)
Alert(title="Warning alert", type="warning", show_icon=True, description='This is an explanation', **theme)
Alert(title="Error alert", type="error", show_icon=True, description='This is an explanation', **theme)
with st.expander("Code"):
        st.code("""
        Alert(title="Success alert", type="success", show_icon=True, description='This is an explanation', **theme)
        Alert(title="Info alert", type="info", show_icon=True, description='This is an explanation', **theme)
        Alert(title="Warning alert", type="warning", show_icon=True, description='This is an explanation', **theme)
        Alert(title="Error alert", type="error", show_icon=True, description='This is an explanation', **theme)
        """)
st.divider()
st.markdown("###### The code used to create the Alert component")
st.code("""
#####  Alert definition

def JS_create_alert_directives(parameters, anchor):
    def f():
        ret = dict()
        ret['title'] = parameters.title
        ret['type'] = parameters.type
        ret['description'] = parameters.description
        ret['closable'] = parameters.closable
        ret['center'] = parameters.center
        ret['effect'] = parameters.effect
        ret['show_icon'] = parameters.show_icon
        ret['close_alert'] = parameters.close_alert
        return ret
    return f

def JS_create_alert_methods(parameters, anchor):
    ret = dict()
    return ret

def create_alert_template():
        ELALERT = gentag("el-alert") 
        options = dict()
        options[':title'] = "title"
        options[':type'] = "type"
        options[':description'] = "description"
        options[':closable'] = "closable"
        options[':center'] = "center"
        options[':effect'] = "effect"
        options[':show-icon'] = "show_icon"
        options[':close-text'] = "close_text"
        return DIV(ELALERT(**options), id="app")

def use_alert(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Alert = GenComponent('ElementPlusAlert', create_alert_template, genscript(JS_create_alert_directives), genscript(JS_create_alert_methods)).encapsulate(use_alert)
""")