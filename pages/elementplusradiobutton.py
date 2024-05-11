import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Radio button", divider="rainbow")
rb1 = dict(label='New York', value='New York', selected=True)
rb2 = dict(label='Washington', value='Washington')
rb3 = dict(label='Los Angeles', value='Los Angeles')
rb4 = dict(label='Chicago', value='Chicago', disabled=True)
radio1 = [rb1, rb2, rb3, rb4]
defaultv = [x['value'] if 'selected' in x and x['selected'] else None for x in radio1][0]
ra1 = RadioButton(buttons=radio1, size="large", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        rb1 = dict(label='New York', value='New York', selected=True)
        rb2 = dict(label='Washington', value='Washington')
        rb3 = dict(label='Los Angeles', value='Los Angeles')
        rb4 = dict(label='Chicago', value='Chicago', disabled=True)
        radio1 = [rb1, rb2, rb3, rb4]
        defaultv = [x['value'] if 'selected' in x and x['selected'] else None for x in radio1][0]
        ra1 = RadioButton(buttons=radio1, size="large", default=defaultv, **theme)
        """)
st.markdown("The value returned by this group of checkboxes is as follows:")
st.code(f'Returned value ===>  :             {ra1.get()}')
st.markdown("###### Some examples of radio buttons:")
ra2 = RadioButton(buttons=radio1, key="ra2", size="large", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        ra2 = RadioButton(buttons=radio1, key="ra2", size="large", default=defaultv, **theme)
        """)
ra2 = RadioButton(buttons=radio1, key="rax2", size="default", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        ra2 = RadioButton(buttons=radio1, key="rax2", size="default", default=defaultv, **theme)
        """)
ra3 = RadioButton(buttons=radio1, key="ra3", size="small", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        ra3 = RadioButton(buttons=radio1, key="ra3", size="small", default=defaultv, **theme)
        """)
ra4 = RadioButton(buttons=radio1, key="ra4", size="large", fill="yellow", disabled=True, default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        ra4 = RadioButton(buttons=radio1, key="ra4", size="large", fill="yellow", disabled=True, default=defaultv, **theme)
        """)
ra5 = RadioButton(buttons=radio1, key="ra5", size="large", fill="red", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        ra5 = RadioButton(buttons=radio1, key="ra5", size="large", fill="red", default=defaultv, **theme)
        """)
ra6 = RadioButton(buttons=radio1, key="ra6", size="large", fill="lightgreen", textcolor="red", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        ra6 = RadioButton(buttons=radio1, key="ra6", size="large", fill="lightgreen", textcolor="red", default=defaultv, **theme)
        """)
st.divider()
st.markdown("###### The code used to create the RadioButton component")
st.code("""
#####  RadioButton definition

def JS_create_radio_button_directives(parameters, anchor):
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

def JS_create_radio_button_methods(parameters, anchor):
    ret = dict()
    def fhandleItem(button):
        Streamlit.setComponentValue(button.value)
    ret['handleItem'] = fhandleItem
    return ret

def create_radio_button_template():
        ELRADIOBUTTON = gentag("el-radio-button")
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
        goptions[':fill'] = "fill"
        goptions[':text-color'] = "textcolor"
        return DIV(ELRADIOGROUP(ELRADIOBUTTON(**boptions), **goptions), id="app")

def use_radio_button(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

RadioButton = GenComponent('ElementPlusRadioButton', create_radio_button_template, genscript(JS_create_radio_button_directives), genscript(JS_create_radio_button_methods)).encapsulate(use_radio_button)
""")