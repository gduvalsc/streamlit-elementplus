import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Tag", divider="rainbow")
st.markdown("The '**Tag**' component visually defines a list of properties. It is possible to remove properties using the '**closable**' attribute, and it is possible to add new properties to the list.")

tag1 = dict(name='Tag 1', type='primary')
tag2 = dict(name='Tag 2', type='success')
tag3 = dict(name='Tag 3', type='info')
tag4 = dict(name='Tag 4', type='warning')
tag5 = dict(name='Tag 5', type='danger')
tags1 = [tag1, tag2, tag3, tag4, tag5]
defaultv = [x['name'] for x in tags1]
t1 = Tag(tags=tags1, label='Tags', size='large', effect='dark', round=True, editable=True, closable=True, default=defaultv, **theme)
st.write(t1.get())
with st.expander("Code"):
        st.code("""
        tag1 = dict(name='Tag 1', type='primary')
        tag2 = dict(name='Tag 2', type='success')
        tag3 = dict(name='Tag 3', type='info')
        tag4 = dict(name='Tag 4', type='warning')
        tag5 = dict(name='Tag 5', type='danger')
        tags1 = [tag1, tag2, tag3, tag4, tag5]
        defaultv = [x['name'] for x in tags1]
        t1 = Tag(tags=tags1, label='Tags', size='large', effect='dark', round=True, editable=True, closable=True, default=defaultv, **theme)
        """)
st.divider()
st.markdown("###### The code used to create the Tag component")
st.code("""
#####  Tag definition

def JS_create_tag_directives(parameters, anchor):
    def f():
        def ftags():
            for b in range(len(parameters.tags)):
                parameters.tags[b].effect = parameters.effect
                parameters.tags[b].size = parameters.size
                parameters.tags[b].round = parameters.round
                parameters.tags[b].closable = parameters.closable
            return parameters.tags
        ret = dict()
        parameters.dynamictags = Vue.ref(ftags())
        ret['tags'] = parameters.dynamictags
        ret['label'] = parameters.label
        ret['space'] = parameters.space
        ret['inputVisible'] = parameters.inputVisible = Vue.ref(false)
        ret['inputValue'] = parameters.inputValue = Vue.ref('')
        ret['editable'] = parameters.editable
        return ret
    return f

def JS_create_tag_methods(parameters, anchor):
    ret = dict()
    def fclick(x):
        result = [b['name'] for b in parameters.tags]
        Streamlit.setComponentValue(result)    
    def fclose(x):
        parameters.dynamictags.value.splice(parameters.dynamictags.value.indexOf(x), 1)
        result = [b['name'] for b in parameters.dynamictags.value]
        Streamlit.setComponentValue(result)
    def fshowinput():
        parameters.inputVisible.value = True
    def fhandleic():
        if parameters.inputValue.value:
            newtag = dict(name=parameters.inputValue.value)
            newtag['effect'] = parameters.effect
            newtag['size'] = parameters.size
            newtag['round'] = parameters.round
            newtag['closable'] = parameters.closable
            parameters.dynamictags.value.append(newtag)
        parameters.inputVisible.value = False
        parameters.inputValue.value = ''
        result = [b['name'] for b in parameters.dynamictags.value]
        Streamlit.setComponentValue(result)

    ret['handleClick'] = fclick
    ret['handleClose'] = fclose
    ret['showInput'] = fshowinput
    ret['handleInputConfirm'] = fhandleic
    return ret

def create_tag_template():
        ELTAG = gentag("el-tag") 
        ELSPACE = gentag("el-space")
        ELINPUT = gentag("el-input")
        ELBUTTON = gentag("el-button")
        soptions = dict()
        soptions[':size'] = "space"
        options = dict()
        options['v-for'] = "tag in tags"
        options[':key'] = "tag.name"
        options[':type'] = "tag.type"
        options[':effect'] = "tag.effect"
        options[':size'] = "tag.size"
        options[':round'] = "tag.round"
        options[':closable'] = "tag.closable"
        options['@click'] = "handleClick(tag)"
        options['@close'] = "handleClose(tag)"
        ioptions = dict()
        ioptions['v-if'] = "inputVisible"
        ioptions['ref'] = "InputRef"
        ioptions['v-model'] = "inputValue"
        ioptions['style'] = "width: 240px"
        ioptions['@keyup.enter'] = "handleInputConfirm"
        boptions = dict()
        boptions['v-else-if'] = "editable"
        boptions['size'] = "default"
        boptions['@click'] = "showInput"
        return DIV(ELSPACE(ELTAG('{{tag.name}}', **options),ELINPUT(**ioptions),ELBUTTON('+', **boptions), **soptions), id="app")


def use_tag(component):
    class Component:
        def __init__(self, default=[], **d):
            result = component(default=default, **d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Tag = GenComponent('ElementPlusTag', create_tag_template, genscript(JS_create_tag_directives), genscript(JS_create_tag_methods)).encapsulate(use_tag)
""")