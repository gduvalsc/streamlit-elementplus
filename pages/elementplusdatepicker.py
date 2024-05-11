import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Date picker", divider="rainbow")
st.markdown("###### Pick a day")
d1 = DatePicker(size='large', type='date', value_format="YYYY-MM-DD", placeholder='Pick a day', **theme)
st.write(d1.get())
with st.expander("Code"):
        st.code("""
        d1 = DatePicker(size='large', type='date', value_format="YYYY-MM-DD", placeholder='Pick a day', **theme)
        """)
st.divider()
st.markdown("###### Pick a week")
d2 = DatePicker(size='large', type='week', value_format="YYYY-MM-DD", placeholder='Pick a week', **theme)
st.write(d2.get())
with st.expander("Code"):
        st.code("""
        d2 = DatePicker(size='large', type='week', value_format="YYYY-MM-DD", placeholder='Pick a week', **theme)
        """)
st.divider()
st.markdown("###### Pick a month")
d3 = DatePicker(size='large', type='month', value_format="YYYY-MM-DD", placeholder='Pick a month', **theme)
st.write(d3.get())
with st.expander("Code"):
        st.code("""
        d3 = DatePicker(size='large', type='month', value_format="YYYY-MM-DD", placeholder='Pick a month', **theme)
        """)
st.divider()
st.markdown("###### Pick a year")
d4 = DatePicker(size='large', type='year', value_format="YYYY-MM-DD", placeholder='Pick a year', **theme)
st.write(d4.get())
with st.expander("Code"):
        st.code("""
        d4 = DatePicker(size='large', type='year', value_format="YYYY-MM-DD", placeholder='Pick a year', **theme)
        """)
st.divider()
st.markdown("###### Pick one or more dates")
d5 = DatePicker(size='large', type='dates', value_format="YYYY-MM-DD", placeholder='Pick several dates', **theme)
st.write(d5.get())
with st.expander("Code"):
        st.code("""
        d5 = DatePicker(size='large', type='dates', value_format="YYYY-MM-DD", placeholder='Pick several dates', **theme)
        """)
st.divider()
st.markdown("###### Pick a range of dates")
d6 = DatePicker(size='large', type='daterange', value_format="YYYY-MM-DD",start_placeholder='Start date', end_placeholder='End date', **theme)
st.write(d6.get())
with st.expander("Code"):
        st.code("""
        d6 = DatePicker(size='large', type='daterange', value_format="YYYY-MM-DD",start_placeholder='Start date', end_placeholder='End date', **theme)
        """)
st.divider()
st.markdown("###### The code used to create the DatePicker component")
st.code("""
#####  DatePicker definition

def JS_create_date_picker_directives(parameters, anchor):
    def f():
        ret = dict()
        ret['value'] = Vue.ref('')
        ret['size'] = parameters.size
        ret['readonly'] = parameters.readonly
        ret['disabled'] = parameters.disabled
        ret['editable'] = parameters.editable
        ret['clearable'] = parameters.clearable
        ret['placeholder'] = parameters.placeholder
        ret['start_placeholder'] = parameters.start_placeholder
        ret['end_placeholder'] = parameters.end_placeholder
        ret['type'] = parameters.type
        ret['format'] = parameters.format
        ret['value_format'] = parameters.value_format
        return ret
    return f

def JS_create_date_picker_methods(parameters, anchor):
    ret = dict()
    def fsetdate(x):
        Streamlit.setComponentValue(JSON.parse(JSON.stringify(x)))
    def fvisiblechange(x):
        if x: Streamlit.setFrameHeight(document.body.scrollHeight) 
        else: Streamlit.setFrameHeight(anchor.iframeHeight)     
    ret['setDate'] = fsetdate
    ret["visiblechange"] = fvisiblechange   
    return ret

def create_date_picker_template():
        ELDATEPICKER = gentag("el-date-picker") 
        options = dict()
        options['v-model'] = "value"
        options[':size'] = "size"
        options[':readonly'] = "readonly"
        options[':disabled'] = "disabled"
        options[':editable'] = "editable"
        options[':clearable'] = "clearable"
        options[':placeholder'] = "placeholder"
        options[':start-placeholder'] = "start_placeholder"
        options[':end-placeholder'] = "end_placeholder"
        options[':type'] = "type"
        options[':format'] = "format"
        options[':value-format'] = "value_format"
        options['@change'] = "setDate"
        options['@visible-change'] = "visiblechange"
        return DIV(ELDATEPICKER(**options), id="app")

def use_date_picker(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

DatePicker = GenComponent('ElementPlusDatePicker', create_date_picker_template, genscript(JS_create_date_picker_directives), genscript(JS_create_date_picker_methods)).encapsulate(use_date_picker)
""")