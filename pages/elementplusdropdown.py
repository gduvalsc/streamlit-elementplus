import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Dropdown", divider="rainbow")
st.markdown("The behavior of a '**dropdown**' widget should be the same as that of a button: the returned value is valid for the duration of an interaction. When the user interacts with another widget, the value of the first widget should revert to **None**. On a '**select**' type widget, the behavior is different: the selected value should remain active across multiple interactions.")
i1 = dict(label='Action 1', command='a1')
i2 = dict(label='Action 2', command='a2')
i3 = dict(label='Action 3', command='a3')
i4 = dict(label='Action 4', command='a4', disabled=True)
i5 = dict(label='Action 5', command='a5', divided=True)
i6 = dict(label='Action 6', command='a6')
i7 = dict(label='Action 7', command='a7', divided=True)
menu = [i1, i2, i3, i4, i5, i6, i7]
col1, col2 = st.columns([1, 1])
with col1:   
    b1 = dict(label='Dropdown List 1', type='info')
    d1 = Dropdown(menu=menu, button=b1, id='b1', **theme)
    st.write(d1.get())
with col2:   
    b2 = dict(label='Dropdown List 2', type='primary')
    d2 = Dropdown(menu=menu, button=b2, id='b2', **theme)
    st.write(d2.get())
with st.expander("Code"):
        st.code("""
        i1 = dict(label='Action 1', command='a1')
        i2 = dict(label='Action 2', command='a2')
        i3 = dict(label='Action 3', command='a3')
        i4 = dict(label='Action 4', command='a4', disabled=True)
        i5 = dict(label='Action 5', command='a5', divided=True)
        i6 = dict(label='Action 6', command='a6')
        i7 = dict(label='Action 7', command='a7', divided=True)
        menu = [i1, i2, i3, i4, i5, i6, i7]
        col1, col2 = st.columns([1, 1])
        with col1:   
            b1 = dict(label='Dropdown List 1', type='info')
            d1 = Dropdown(menu=menu, button=b1, id='b1', **theme)
            st.write(d1.get())
        with col2:   
            b2 = dict(label='Dropdown List 2', type='primary')
            d2 = Dropdown(menu=menu, button=b2, id='b2', **theme)
            st.write(d2.get())
        """)
st.divider()
st.markdown("###### The code used to create the Dropdown component")
st.code("""
#####  Dropdown definition

def JS_create_dropdown_directives(parameters, anchor):
    def f():
        ret = dict()
        def fmenu():
            return Vue.reactive(parameters.menu)
        ret['menu'] = fmenu()
        ret["btype"] = parameters.button['type']
        ret["label"] = parameters.button['label']
        return ret
    return f

def JS_create_dropdown_methods(parameters, anchor):
    def foverbutton():
        Streamlit.setFrameHeight(document.body.scrollHeight)    
    def fcommand(x):
        result = {'counter': parameters.counter + 1, 'value': x}
        console.log(result)
        Streamlit.setComponentValue(result)
    ret = dict()    
    def fvisiblechange(x):
        if x: Streamlit.setFrameHeight(document.body.scrollHeight) 
        else: Streamlit.setFrameHeight(anchor.iframeHeight) 
    ret = dict()
    ret["overbutton"] = foverbutton        
    ret["command"] = fcommand    
    ret["visiblechange"] = fvisiblechange    
    return ret

def create_dropdown_template():
        TEMPLATE = gentag("template") 
        ELDROPDOWN = gentag("el-dropdown") 
        ELDROPDOWNMENU = gentag("el-dropdown-menu") 
        ELDROPDOWNITEM = gentag("el-dropdown-item") 
        ELBUTTON = gentag("el-button") 
        options = dict()
        boptions = dict()
        ioptions = dict()
        boptions[':type'] = "btype"
        boptions['class'] = "el-dropdown-link"
        boptions['@click'] = "overbutton"
        options['@command'] = "command"
        options['@visible-change'] = "visiblechange"
        ioptions['v-for'] = "item in menu"
        ioptions[':disabled'] = "item.disabled"
        ioptions[':divided'] = "item.divided"
        ioptions[':command'] = "item.command"
        return DIV(ELDROPDOWN(ELBUTTON('{{label}}', **boptions), TEMPLATE(ELDROPDOWNMENU(ELDROPDOWNITEM('{{item.label}}' ,**ioptions)), **{'#dropdown': True}), **options), id="app")

def use_dropdown(component):
    class Component:
        def __init__(self, id=None, **d):
            id = f'Component_{id}'
            if id not in st.session_state: st.session_state[id] = dict(old=0, new=0)
            result = component(id=id, counter=st.session_state[id]['new'], **d)
            if result and 'counter' in result and result['counter'] != st.session_state[id]['new']:
                st.session_state[id]['new'] = result['counter']
                st.session_state[id]['result'] = result['value']
                st.rerun()
            if st.session_state[id]['old'] != st.session_state[id]['new']:
                self.result = st.session_state[id]['result']
                st.session_state[id]['old'] = st.session_state[id]['new']
            else: self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component


Dropdown = GenComponent('ElementPlusDropdown', create_dropdown_template, genscript(JS_create_dropdown_directives), genscript(JS_create_dropdown_methods)).encapsulate(use_dropdown)
""")