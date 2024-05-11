import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Color picker", divider="rainbow")
st.markdown("###### Color picker returning a color in format rgba")
predefine=['rgb(0,0,0)', 'rgb(0,0,255)', 'rgb(0,255,0)', 'rgb(0,255,255)', 'rgb(255,0,0)', 'rgb(255,0,255)', 'rgb(255,255,0)', 'rgb(255,255,255)']
c1 = ColorPicker(size='large', key="a", showalpha=True, predefine=predefine, default='rgba(19, 206, 102, 0.8)', **theme)
st.write(c1.get())
with st.expander("Code"):
        st.code("""
        predefine=['rgb(0,0,0)', 'rgb(0,0,255)', 'rgb(0,255,0)', 'rgb(0,255,255)', 'rgb(255,0,0)', 'rgb(255,0,255)', 'rgb(255,255,0)', 'rgb(255,255,255)']
        c1 = ColorPicker(size='large', key="a", showalpha=True, predefine=predefine, default='rgba(19, 206, 102, 0.8)', **theme)
        """)
st.divider()
st.markdown("###### Color picker returning a color in format hex")
c2 = ColorPicker(size='large', key="b", showalpha=False, format='hex', default='#FFFF00', **theme)
st.write(c2.get())
with st.expander("Code"):
        st.code("""
        c2 = ColorPicker(size='large', key="b", showalpha=False, format='hex', default='#FFFF00', **theme)
        """)
st.divider()
st.markdown("###### The code used to create the ColorPicker component")
st.code("""
#####  ColorPicker definition

def JS_create_color_picker_directives(parameters, anchor):
    def f():
        ret = dict()
        ret['color'] = Vue.ref(parameters.default)
        ret['size'] = parameters.size
        ret['disabled'] = parameters.disabled
        ret['showalpha'] = parameters.showalpha
        ret['predefine'] = Vue.ref(parameters.predefine)
        ret['colorformat'] = parameters.colorformat
        return ret
    return f

def JS_create_color_picker_methods(parameters, anchor):
    ret = dict()
    def fdefine(x):
        Streamlit.setFrameHeight(anchor.iframeHeight) 
        Streamlit.setComponentValue(x)      
    def fpick(x):
        Streamlit.setFrameHeight(document.body.scrollHeight)     
    ret['pickColor'] = fpick
    ret['defineColor'] = fdefine
    ret['blur'] = fpick
    return ret

def create_color_picker_template():
        ELCOLORPICKER = gentag("el-color-picker") 
        options = dict()
        options['v-model'] = "color"
        options[':size'] = "size"
        options[':disabled'] = "disabled"
        options[':show-alpha'] = "showalpha"
        options[':color-format'] = "colorformat"
        options[':predefine'] = "predefine"
        options['@active-change'] = "pickColor"
        options['@change'] = "defineColor"
        options['@blur'] = "blur"
        return DIV(ELCOLORPICKER(**options), id="app")

def use_color_picker(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

ColorPicker = GenComponent('ElementPlusColorPicker', create_color_picker_template, genscript(JS_create_color_picker_directives), genscript(JS_create_color_picker_methods)).encapsulate(use_color_picker)
""")

