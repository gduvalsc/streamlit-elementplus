import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Button Group", divider="rainbow")
st.markdown("Generating unit components like buttons that only return 2 values (true or false) is relatively straightforward from a data management perspective, but it can be a drawback in terms of the application's rendering: each component occupies space in the visual output, which can be a disadvantage in the application's usability.")
st.markdown(("It can be interesting to create components like this one:"))
button1 = dict(label='Button 1',id='button1')
button2 = dict(label='Button 2',id='button2')
buttons1 = [button1, button2]
bg1 = ButtonGroup(buttons=buttons1, type='primary', id='bg1', default={x['id']:False for x in buttons1})
with st.expander("Code"):
        st.code("""
        button1 = dict(label='Button 1',id='button1')
        button2 = dict(label='Button 2',id='button2')
        buttons1 = [button1, button2]
        bg1 = ButtonGroup(buttons=buttons1, type='primary', id='bg1', default={x['id']:False for x in buttons1})
        """)
st.markdown(("or this one:"))
button1 = dict(icon='Edit', id='button1')
button2 = dict(icon='Share', id='button2')
button3 = dict(label='Delete', icon='Delete', id='button3', type='danger')
buttons2 = [button1, button2, button3]
bg2 = ButtonGroup(buttons=buttons2, type='primary', id='bg2', default={x['id']:False for x in buttons2})
with st.expander("Code"):
        st.code("""
        button1 = dict(icon='Edit', id='button1')
        button2 = dict(icon='Share', id='button2')
        button3 = dict(label='Delete', icon='Delete', id='button3', type='danger')
        buttons2 = [button1, button2, button3]
        bg2 = ButtonGroup(buttons=buttons2, type='primary', id='bg2', default={x['id']:False for x in buttons2})
        """)
st.markdown("In this case, the visual rendering part is slightly more complex. You need to use the 'v-for' directive of Vue.js to specify the number of elements to render. Each element must have an 'id' that distinguishes it from other elements composing the group.")
st.markdown("The rendering is also more complex: if there are n buttons, only one of them can render the value true! The others must render the value false. The return structure is a dictionary that includes the id of the buttons and renders true or false for each button. The 'ButtonGroup' component is not a 'CheckboxButton'. In the case of a 'ButtonGroup', only one button can render true. In a 'CheckboxButton', multiple buttons can return the value true.")
st.markdown('Example:')
col1, col2 = st.columns([1,1])
with col1:
    button1 = dict(label='Button 1',id='button1')
    button2 = dict(label='Button 2',id='button2')
    buttons1 = [button1, button2]
    bg1 = ButtonGroup(buttons=buttons1, type='primary', id='bg1x', default={x['id']:False for x in buttons1})
    st.write(bg1.get())
with col2:
    button3 = dict(label='Button 3',id='button3')
    button4 = dict(label='Button 4',id='button4')
    buttons2 = [button3, button4]
    bg2 = ButtonGroup(buttons=buttons2, type='primary', id='bg2x', default={x['id']:False for x in buttons2})
    st.write(bg2.get())

st.divider()
st.markdown("###### The code used to create the ButtonGroup component")
st.code("""
####  ButtonGroup definition

def JS_create_button_group_directives(parameters):
    def f():
        def fbuttons():
            for b in range(len(parameters.buttons)):
                if hasattr(parameters.buttons[b], "icon"):
                    console.log('before', parameters.buttons[b].icon)
                    parameters.buttons[b].iconx = Vue.shallowRef(ElementPlusIconsVue[parameters.buttons[b].icon])
                    console.log('after', parameters.buttons[b].iconx)

            return Vue.reactive(parameters.buttons)   
        ret = dict()
        ret['buttons'] = fbuttons()
        ret['type'] = parameters.type
        ret['size'] = parameters.size
        return ret
    return f

def JS_create_button_group_methods(parameters):
    ret = dict()
    def fhandleItem(button):
        result = {'counter': parameters.counter + 1}
        for b in parameters.buttons:
            if b['id'] == button['id']: result[b['id']] = True
            else: result[b['id']] = False
        Streamlit.setComponentValue(result)
    ret['handleItem'] = fhandleItem
    return ret

def create_button_group_template():
        ELBUTTON = gentag("el-button")
        ELBUTTONGROUP = gentag("el-button-group")
        boptions = dict()
        goptions = dict()
        boptions['v-for'] = "button in buttons"
        boptions[':type'] = "button.type"
        boptions[':icon'] = "button.iconx"
        boptions[':key'] = "button.id"
        boptions['@click'] = "handleItem(button)"
        goptions[':type'] = "type"
        goptions[':size'] = "size"
        return DIV(ELBUTTONGROUP(ELBUTTON('{{button.label}}', **boptions), **goptions), id="app")

def use_button_group(component):
    class Component:
        def __init__(self, buttons=[], type='default', size='default', id=None, default=None):
            id = f'Component_{id}'
            if id not in st.session_state: st.session_state[id] = dict(old=0, new=0)
            result = component(id=id, type=type, buttons=buttons, size=size, counter=st.session_state[id]['new'], default=default)
            if 'counter' in result and result['counter'] != st.session_state[id]['new']:
                st.session_state[id]['new'] = result['counter']
                st.session_state[id]['result'] = result
                del st.session_state[id]['result']['counter']
                st.rerun()
            if st.session_state[id]['old'] != st.session_state[id]['new']:
                self.result = st.session_state[id]['result']
                st.session_state[id]['old'] = st.session_state[id]['new']
            else: self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

ButtonGroup = GenComponent('ElementPlusButtonGroup', create_button_group_template, genscript(JS_create_button_group_directives), genscript(JS_create_button_group_methods)).encapsulate(use_button_group)
""")

