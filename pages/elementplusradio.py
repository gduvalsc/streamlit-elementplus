import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
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
ra1 = Radio(buttons=radio1, size="large", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        rb1 = dict(label='New York', value='New York', selected=True)
        rb2 = dict(label='Washington', value='Washington')
        rb3 = dict(label='Los Angeles', value='Los Angeles')
        rb4 = dict(label='Chicago', value='Chicago', disabled=True)
        radio1 = [rb1, rb2, rb3, rb4]
        defaultv = [x['value'] if 'selected' in x and x['selected'] else None for x in radio1][0]
        ra1 = Radio(buttons=radio1, size="large", default=defaultv, **theme)
        """)
st.markdown("The value returned by this group of checkboxes is as follows:")
st.code(f'Returned value ===>  :             {ra1.get()}')
st.markdown("###### Some examples of radio buttons:")
ra2 = Radio(buttons=radio1, key="ra2", size="large", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        ra2 = Radio(buttons=radio1, key="ra2", size="large", default=defaultv, **theme)
        """)
ra3 = Radio(buttons=radio1, key="ra3", size="small", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        ra3 = Radio(buttons=radio1, key="ra3", size="small", default=defaultv, **theme)
        """)
ra4 = Radio(buttons=radio1, key="ra4", size="large", disabled=True, default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        ra4 = Radio(buttons=radio1, key="ra4", size="large", disabled=True, default=defaultv, **theme)
        """)
st.divider()
st.markdown("###### The code used to create the Radio component")
st.code("""
#####  Radio definition

def JS_create_radio_directives(parameters, anchor):
    def f():
        def fbuttons():
            return Vue.reactive(parameters.buttons)
        def fradio():
            result = None
            for b in range(len(parameters.buttons)):
                if hasattr(parameters.buttons[b], "selected") and parameters.buttons[b].selected: result = parameters.buttons[b].value
            return Vue.ref(result)
        ret = dict()
        ret['buttons'] = fbuttons()
        ret['radio'] = fradio()
        ret['size'] = parameters.size
        ret['label'] = parameters.label
        ret['disabled'] = parameters.disabled
        ret['min'] = parameters.min
        ret['max'] = parameters.max
        ret['fill'] = parameters.fill
        ret['textcolor'] = parameters.textcolor
        return ret
    return f

def JS_create_radio_methods(parameters, anchor):
    ret = dict()
    def fhandleItem(button):
        Streamlit.setComponentValue(button.value)
    ret['handleItem'] = fhandleItem
    return ret

def create_radio_template():
        ELRADIO = gentag("el-radio")
        ELRADIOGROUP = gentag("el-radio-group")
        boptions = dict()
        goptions = dict()
        boptions['v-for'] = "button in buttons"
        boptions[':label'] = "button.label"
        boptions[':key'] = "button.value"
        boptions[':border'] = "button.border"
        boptions[':disabled'] = "button.disabled"
        boptions['@change'] = "handleItem(button)"
        goptions['v-model'] = "radio"
        goptions[':size'] = "size"
        goptions[':label'] = "label"
        goptions[':disabled'] = "disabled"
        return DIV(ELRADIOGROUP(ELRADIO(**boptions), **goptions), id="app")

def use_radio(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Radio = GenComponent('ElementPlusRadio', create_radio_template, genscript(JS_create_radio_directives), genscript(JS_create_radio_methods)).encapsulate(use_radio)
""")