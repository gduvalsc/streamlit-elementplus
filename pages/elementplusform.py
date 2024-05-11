import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

theme = set_page_config()
gen_back_button()

st.subheader("Form", divider="rainbow")

def create_form1_template():
        ELFORM = gentag("el-form")
        ELFORMITEM = gentag("el-form-item")
        ELINPUT = gentag("el-input")
        ELSELECT = gentag("el-select")
        ELOPTION = gentag("el-option")
        ELCOL = gentag("el-col")
        ELDATEPICKER = gentag("el-date-picker")
        ELTIMEPICKER = gentag("el-time-picker")
        ELSWITCH = gentag("el-switch")
        ELCHECKBOXGROUP = gentag("el-checkbox-group")
        ELCHECKBOX = gentag("el-checkbox")
        ELRADIOGROUP = gentag("el-radio-group")
        ELRADIO = gentag("el-radio")
        ELBUTTON = gentag("el-button")
        SPAN = gentag("span")
        foptions = {':model':"form", 'label-width':"auto", 'style':"max-width: 600px"}
        fiopt1 = {'label': "Activity name"}
        fiopt2 = {'label': "Activity zone"}
        fiopt3 = {'label': "Activity time"}
        fiopt4 = {'label': "Instant delivery"}
        fiopt5 = {'label': "Activity type"}
        fiopt6 = {'label': "Resources"}
        fiopt7 = {'label': "Activity form"}
        inpopt1 = {'v-model': "form.name"}
        inpopt2 = {'v-model': "form.desc", 'type':"textarea"}
        selopt = {'v-model': "form.region", 'placeholder': "please select your zone"}
        colopt1 = {':span': "11"}
        colopt2 = {':span': "2", 'class': "text-center"}
        spanopt1 = {'class': "text-gray-500"}
        datepopt = {'v-model': "form.date1", 'placeholder': "Pick a date", 'type': "date", 'style': "width: 100%"}
        timepopt = {'v-model': "form.date2", 'placeholder': "Pick a time", 'style': "width: 100%"}
        swiopt = {'v-model': "form.delivery"}
        cbgopt = {'v-model': "form.type"}
        ragopt = {'v-model': "form.resource"}
        option1 = ELOPTION(label="Zone one", value="New York")
        option2 = ELOPTION(label="Zone two", value="Paris")
        cb1 = ELCHECKBOX('Online activities', value="Online activities", name="type")
        cb2 = ELCHECKBOX('Promotion activities', value="Promotion activities", name="type")
        cb3 = ELCHECKBOX('Offline activities', value="Offline activities", name="type")
        cb4 = ELCHECKBOX('Simple brand exposure', value="Simple brand exposure", name="type")
        ra1 = ELRADIO('Sponsor', value="Sponsor")
        ra2 = ELRADIO('Venue', value="Venue")
        fitem1 = ELFORMITEM(ELINPUT(**inpopt1),**fiopt1)
        fitem2 = ELFORMITEM(ELSELECT(option1, option2, **selopt), **fiopt2)
        fitem3 = ELFORMITEM(ELCOL(ELDATEPICKER(**datepopt), **colopt1), ELCOL(SPAN('-', **spanopt1), **colopt2), ELCOL(ELTIMEPICKER(**timepopt), **colopt1), **fiopt3)
        fitem4 = ELFORMITEM(ELSWITCH(**swiopt), **fiopt4)
        fitem5 = ELFORMITEM(ELCHECKBOXGROUP(cb1, cb2, cb3, cb4, **cbgopt), **fiopt5)
        fitem6 = ELFORMITEM(ELRADIOGROUP(ra1, ra2, **ragopt), **fiopt6)
        fitem7 = ELFORMITEM(ELINPUT(**inpopt2), **fiopt7)
        fitem8 = ELFORMITEM(ELBUTTON('Create', type="primary", **{'@click':"submit"}))
        return DIV(ELFORM(fitem1, fitem2, fitem3, fitem4, fitem5, fitem6, fitem7, fitem8, **foptions), id="app")

def JS_create_form1_directives(parameters, anchor):
    def f():
        ret = dict()
        ret['form'] = dict()
        ret['form']['name'] = parameters.name
        ret['form']['region'] = ''
        ret['form']['date1'] = ''
        ret['form']['date2'] = ''
        ret['form']['delivery'] = parameters.delivery
        ret['form']['type'] = []
        ret['form']['resource'] = ''
        ret['form']['desc'] = ''
        anchor.form = ret['form']
        return ret
    return f

def JS_create_form1_methods(parameters, anchor):
    def fsubmit():
        Streamlit.setComponentValue(anchor.form)
    ret = dict()
    ret['submit'] = fsubmit
    return ret

def use_form1(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Form1 = GenComponent('ElementPlusForm1', create_form1_template, genscript(JS_create_form1_directives), genscript(JS_create_form1_methods)).encapsulate(use_form1)

x = Form1(name='abcd', delivery=False, **theme)

st.write(x.get())
