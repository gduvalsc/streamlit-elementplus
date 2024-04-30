import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Button", divider="rainbow")
st.markdown("###### Two buttons in action and their return values")
col1, col2 = st.columns([1,1])
with col1:
    b1 = Button(label='Button 1', type='primary', id='b1')
    st.write(b1.get())
with col2:
    b2 = Button(label='Button 2', type='success', id='b2')
    st.write(b2.get())
with st.expander("Code"):
        st.code("""
col1, col2 = st.columns([1,1])
with col1:
    b1 = Button(label='Button 1', type='primary', id='b1')
    st.write(b1.get())
with col2:
    b2 = Button(label='Button 2', type='success', id='b2')
    st.write(b2.get())
        """)
st.markdown("In general, a component like a button is instantiated as follows: **x = Button(...)** and its return value is retrieved using the get method: **x.get()**.")
st.markdown("For a button, the return value is true or false, and this value is reset when Streamlit automatically replays the script.")
st.markdown("Thus, our 'Element Plus' button behaves exactly the same as the standard 'st.button'.")
st.markdown("The added value of the Element Plus button lies mainly in the rendering options of the button, particularly the ability to integrate an icon.")
st.divider()
st.markdown("###### Examples of buttons")
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
    Button(label='Default')
with col2:
    Button(label='Primary', type='primary')
with col3:
    Button(label='Success', type='success')
with col4:
    Button(label='Info', type='info')
with col5:
    Button(label='Warning', type='warning')
with col6:
    Button(label='Danger', type='danger')  
with st.expander("Code"):
        st.code("""
        Button(label='Default')
        Button(label='Primary', type='primary')
        Button(label='Success', type='success')
        Button(label='Info', type='info')
        Button(label='Warning', type='warning')
        Button(label='Danger', type='danger')  
        """)
st.divider()
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
    Button(label='Plain', plain=True)
with col2:
    Button(label='Primary', type='primary', plain=True)
with col3:
    Button(label='Success', type='success', plain=True)
with col4:
    Button(label='Info', type='info', plain=True)
with col5:
    Button(label='Warning', type='warning', plain=True)
with col6:
    Button(label='Danger', type='danger', plain=True)    
with st.expander("Code"):
        st.code("""
        Button(label='Plain', plain=True)
        Button(label='Primary', type='primary', plain=True)
        Button(label='Success', type='success', plain=True)
        Button(label='Info', type='info', plain=True)
        Button(label='Warning', type='warning', plain=True)
        Button(label='Danger', type='danger', plain=True)    
        """)
st.divider()
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
    Button(label='Round', round=True)
with col2:
    Button(label='Primary', type='primary', round=True)
with col3:
    Button(label='Success', type='success', round=True)
with col4:
    Button(label='Info', type='info', round=True)
with col5:
    Button(label='Warning', type='warning', round=True)
with col6:
    Button(label='Danger', type='danger', round=True)
with st.expander("Code"):
        st.code("""
        Button(label='Round', round=True)
        Button(label='Primary', type='primary', round=True)
        Button(label='Success', type='success', round=True)
        Button(label='Info', type='info', round=True)
        Button(label='Warning', type='warning', round=True)
        Button(label='Danger', type='danger', round=True)
        """)
st.divider()
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
    Button(label='Disabled', round=True, disabled=True)
with col2:
    Button(label='Primary', type='primary', round=True, disabled=True)
with col3:
    Button(label='Success', type='success', round=True, disabled=True)
with col4:
    Button(label='Info', type='info', round=True, disabled=True)
with col5:
    Button(label='Warning', type='warning', round=True, disabled=True)
with col6:
    Button(label='Danger', type='danger', round=True, disabled=True)
with st.expander("Code"):
        st.code("""
        Button(label='Disabled', round=True, disabled=True)
        Button(label='Primary', type='primary', round=True, disabled=True)
        Button(label='Success', type='success', round=True, disabled=True)
        Button(label='Info', type='info', round=True, disabled=True)
        Button(label='Warning', type='warning', round=True, disabled=True)
        Button(label='Danger', type='danger', round=True, disabled=True)
        """)
st.divider()
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
    Button(label='Text', link=True)
with col2:
    Button(label='Primary', type='primary', link=True)
with col3:
    Button(label='Success', type='success', link=True)
with col4:
    Button(label='Info', type='info', link=True)
with col5:
    Button(label='Warning', type='warning', link=True)
with col6:
    Button(label='Danger', type='danger', link=True)
with st.expander("Code"):
        st.code("""
        Button(label='Text', link=True)
        Button(label='Primary', type='primary', link=True)
        Button(label='Success', type='success', link=True)
        Button(label='Info', type='info', link=True)
        Button(label='Warning', type='warning', link=True)
        Button(label='Danger', type='danger', link=True)
        """)
st.divider()
col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
with col1:
    Button(icon='Search', circle=True)
with col2:
    Button(icon='Edit', type='primary', circle=True)
with col3:
    Button(icon='Check', type='success', circle=True)
with col4:
    Button(icon='Message', type='info', circle=True)
with col5:
    Button(icon='Star', type='warning', circle=True)
with col6:
    Button(icon='Delete', type='danger', circle=True)
with st.expander("Code"):
        st.code("""
        Button(icon='Search', circle=True)
        Button(icon='Edit', type='primary', circle=True)
        Button(icon='Check', type='success', circle=True)
        Button(icon='Message', type='info', circle=True)
        Button(icon='Star', type='warning', circle=True)
        Button(icon='Delete', type='danger', circle=True)
        """)
st.divider()
st.markdown("Of course, it's possible to combine buttons with both an icon and text. For instance, this 'Back' button which allows you to return to the main page:")
back = Button(label='Back', icon='ArrowLeftBold', type='danger', id='back')
if back.get(): 
    switch_page('main')
st.divider()
st.markdown("###### The code used to create the Button component")
st.code("""
#####  Button definition

def JS_create_button_directives(parameters):
    def f():
        ret = dict()
        ret['label'] = parameters.label
        ret['link'] = parameters.link
        ret['type'] = parameters.type
        ret['size'] = parameters.size
        ret['round'] = parameters.round
        ret['plain'] = parameters.plain
        ret['disabled'] = parameters.disabled
        ret['circle'] = parameters.circle
        ret['icon'] = Vue.shallowRef(ElementPlusIconsVue[parameters.icon])
        return ret
    return f

def JS_create_button_methods(parameters):
    ret = dict()
    def fgetValue():
        Streamlit.setComponentValue(parameters.counter+1)
    ret['getValue'] = fgetValue
    return ret

def create_button_template():
        ELBUTTON = gentag("el-button")
        options = dict()
        ifoptions = dict()
        elseoptions = dict()
        options[':circle'] = "circle"
        options[':disabled'] = "disabled"
        options[':plain'] = "plain"
        options[':round'] = "round"
        options[':link'] = "link"
        options[':type'] = "type"
        options[':size'] = "size"
        options[':icon'] = "icon"
        options['@click'] = "getValue"
        ifoptions['v-if'] = "label !== null"
        elseoptions['v-else'] = True
        return DIV(ELBUTTON('{{label}}', **options, **ifoptions),ELBUTTON(**options, **elseoptions), id="app")

def use_button(component):
    class Component:
        def __init__(self, label=None, type='default', round=False, circle=False, plain=False, disabled=False, link=False, size='default', icon=None, id=None):
            id = f'Component_{id}'
            if id not in st.session_state: st.session_state[id] = dict(old=0, new=0)
            result = component(label=label, type=type, round=round, circle=circle, plain=plain, disabled=disabled, link=link, size=size, icon=icon, id=id, counter=st.session_state[id]['new'], default=st.session_state[id]['new'])
            if result != st.session_state[id]['new']:
                st.session_state[id]['new'] = result
                st.rerun()
            if st.session_state[id]['old'] != st.session_state[id]['new']:
                self.result = True
                st.session_state[id]['old'] = st.session_state[id]['new']
            else: self.result = False
        def get(self):
            return self.result
    return Component

Button = GenComponent('ElementPlusButton', create_button_template, genscript(JS_create_button_directives), genscript(JS_create_button_methods)).encapsulate(use_button)

""")