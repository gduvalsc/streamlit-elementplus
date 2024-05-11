import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
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
cbg1 = CheckboxButton(checkboxes=checkb1, size="large", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        cb1 = dict(label='Option A', truevalue='Value true A', falsevalue='Value false A', selected=True, id='a')
        cb2 = dict(label='Option B', truevalue='Value true B', falsevalue='Value false B', id='b')
        cb3 = dict(label='Option C', truevalue='Value true C', falsevalue='Value false C', id='c')
        cb4 = dict(label='Disabled', truevalue='Value true D', falsevalue='Value false D', disabled=True, id='d')
        cb5 = dict(label='Selected and disabled', truevalue='Value true E', falsevalue='Value false E', disabled=True, selected=True, id='e')
        checkb1 = [cb1, cb2, cb3, cb4, cb5]
        defaultv = {x['id']:x['truevalue'] if 'selected' in x and x['selected'] else x['falsevalue'] for x in checkb1}
        cbg1 = CheckboxButton(checkboxes=checkb1, size="large", default=defaultv, **theme)
        """)
st.markdown("The value returned by this group of checkboxes is as follows:")
st.write(cbg1.get())
st.markdown("###### Some examples of checkboxes:")
CheckboxButton(checkboxes=checkb1, key='cbg2', size="large", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg2', size="large", default=defaultv, **theme)
        """)
CheckboxButton(checkboxes=checkb1, key='cbg3', size="small", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg3', size="small", default=defaultv, **theme)
        """)
CheckboxButton(checkboxes=checkb1, key='cbg4', disabled=True, default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg4', disabled=True, default=defaultv, **theme)
        """)
CheckboxButton(checkboxes=checkb1, key='cbg5', fill="red", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg5', fill="red", default=defaultv, **theme)
        """)
CheckboxButton(checkboxes=checkb1, key='cbg6', fill="lightgreen", textcolor="red", default=defaultv, **theme)
with st.expander("Code"):
        st.code("""
        CheckboxButton(checkboxes=checkb1, key='cbg6', fill="lightgreen", textcolor="red", default=defaultv, **theme)
        """)
st.divider()
st.markdown("###### The code used to create the CheckboxButton component")
st.code("""

#####  CheckboxButton definition

def JS_create_checkbox_button_directives(parameters, anchor):
    def f():
        def fcheckboxes():
            for b in range(len(parameters.checkboxes)): anchor.state[parameters.checkboxes[b].id] = parameters.checkboxes[b]
            return Vue.reactive(parameters.checkboxes)
        def fchecklist():
            result = []
            for b in range(len(parameters.checkboxes)):
                if hasattr(parameters.checkboxes[b], "selected"):
                    if parameters.checkboxes[b].selected:
                        parameters.checkboxes[b].val = parameters.checkboxes[b].truevalue
                        result.append(parameters.checkboxes[b].truevalue)
                    else: parameters.checkboxes[b].val = parameters.checkboxes[b].falsevalue
                else: parameters.checkboxes[b].val = parameters.checkboxes[b].falsevalue
            return Vue.ref(result)
        ret = dict()
        ret['checkboxes'] = fcheckboxes()
        ret['checklist'] = fchecklist()
        ret['size'] = parameters.size
        ret['label'] = parameters.label
        ret['disabled'] = parameters.disabled
        ret['min'] = parameters.min
        ret['max'] = parameters.max
        ret['fill'] = parameters.fill
        ret['textcolor'] = parameters.textcolor
        return ret
    return f

def JS_create_checkbox_button_methods(parameters, anchor):
    ret = dict()
    def fhandleItem(checkbox):
        result = dict()
        for b in anchor.state:
            if anchor.state[b].id == checkbox.id:
                if anchor.state[b].val == anchor.state[b].truevalue: anchor.state[b].val = anchor.state[b].falsevalue
                else: anchor.state[b].val = anchor.state[b].truevalue
            result[b] = anchor.state[b].val
        Streamlit.setComponentValue(result)
    ret['handleItem'] = fhandleItem
    return ret

def create_checkbox_button_template():
        ELCHECKBOXBUTTON = gentag("el-checkbox-button")
        ELCHECKBOXGROUP = gentag("el-checkbox-group")
        coptions = dict()
        goptions = dict()
        coptions['v-for'] = "checkbox in checkboxes"
        coptions[':label'] = "checkbox.label"
        coptions[':key'] = "checkbox.id"
        coptions[':checked'] = "checkbox.selected"
        coptions[':border'] = "checkbox.border"
        coptions[':disabled'] = "checkbox.disabled"
        coptions['@change'] = "handleItem(checkbox)"
        goptions['v-model'] = "checklist"
        goptions[':size'] = "size"
        goptions[':label'] = "label"
        goptions[':disabled'] = "disabled"
        goptions[':fill'] = "fill"
        goptions[':text-color'] = "textcolor"
        return DIV(ELCHECKBOXGROUP(ELCHECKBOXBUTTON(**coptions), **goptions), id="app")

def use_checkbox_button(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

CheckboxButton = GenComponent('ElementPlusCheckboxButton', create_checkbox_button_template, genscript(JS_create_checkbox_button_directives), genscript(JS_create_checkbox_button_methods)).encapsulate(use_checkbox_button)
""")
