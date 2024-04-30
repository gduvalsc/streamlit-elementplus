import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()

st.subheader("Streamlit components based on Element Plus and Vue.js", divider="rainbow")
st.markdown("""
This Streamlit application aims to achieve two objectives:
1. **Provide components** based on '**Element Plus**' and '**Vue.js**' technology that can be used within Streamlit.
2. **Define an alternative method** to the commonly used approach for extending Streamlit with new components.
""")
st.markdown("Element Plus is a JavaScript framework that enables easily defining sophisticated widgets using Vue.js (https://element-plus.org/en-US/).")
st.markdown("""There are 2 categories of users:
1. Those seeking more or less sophisticated components for their application needs and who do not want to know how these components are made.
2. Those seeking to understand how components are made in order to eventually modify them or create other components.
""")
st.markdown("For the first category of users, they can stop reading at this point and browse the various components offered by pressing the following buttons:")

st.session_state.caller="main"
button1 = dict(label='Button',id='button')
button2 = dict(label='Button Group',id='buttong')
button3 = dict(label='Checkbox',id='checkbox')
button4 = dict(label='Checkbox Button',id='checkboxb')
button5 = dict(label='Radio',id='radio')
button6 = dict(label='Radio Button',id='radiob')
buttonsl1 = [button1, button2, button3, button4, button5, button6]
defaultv = {x['id']:False for x in buttonsl1}
bg1 = ButtonGroup(buttons=buttonsl1, type='primary', id='bg1', default=defaultv)
if bg1.get()['button']: switch_page('elementplusbutton')
if bg1.get()['buttong']: switch_page('elementplusbuttongroup')
if bg1.get()['checkbox']: switch_page('elementpluscheckbox')
if bg1.get()['checkboxb']: switch_page('elementpluscheckboxbutton')
if bg1.get()['radio']: switch_page('elementplusradio')
if bg1.get()['radiob']: switch_page('elementplusradiobutton')
button1 = dict(label='Cascader',id='cascader')
button2 = dict(label='Tag',id='tag')
buttonsl2 = [button1, button2]
defaultv = {x['id']:False for x in buttonsl2}
bg2 = ButtonGroup(buttons=buttonsl2, type='primary', id='bg2', default=defaultv)
if bg2.get()['cascader']: switch_page('elementpluscascader')
if bg2.get()['tag']: switch_page('elementplustag')

st.markdown("For the second category of users, those who seek to understand how this was accomplished, here is the most comprehensive explanation possible:")
st.markdown("Creating an external Streamlit component involves creating an HTML page. I find the method generally used and documented in Streamlit confusing and complex. Employing templates, npm, React, and delivering a Python package installable via pip is a rather sophisticated and daunting contraption, especially for novices")
st.markdown("Instead, I propose the following method which allows defining sophisticated components while staying within Python and with little to no JavaScript:")
st.markdown("When talking about generating an HTML page, it implies generating HTML tags and JavaScript code.")
st.markdown("In the method at hand, to generate the page, we will use a Python package called '**htmlgenerator**' to generate the tags and another Python package called '**pscript**' to generate the JavaScript code.")
st.markdown("An example of using **htmlgenerator**")
st.code('DIV(P("Hello world!"), id="app")')
st.markdown("After rendering, the generated HTML will be:")
st.code("""
<div id="app">
<p>
hello world!
</p>
</div>
""")
st.markdown("An example of using **pscript**. The following python program:")
st.code("""
import pscript, inspect

def JS_create_button_methods(parameters):
    ret = dict()
    def fgetValue():
        Streamlit.setComponentValue(parameters.counter+1)
    ret['getValue'] = fgetValue
    return ret

print(pscript.py2js(inspect.getsource(JS_create_button_methods)))
""")
st.markdown("After being executed, the following string will be rendered:")
st.code("""
var JS_create_button_methods;
JS_create_button_methods = function flx_JS_create_button_methods (parameters) {
    var fgetValue, ret;
    ret = {};
    fgetValue = (function flx_fgetValue () {
        Streamlit.setComponentValue(parameters.counter + 1);
        return null;
    }).bind(this);

    ret["getValue"] = fgetValue;
    return ret;
};
""")
st.markdown("In the previous Python program, the function '**JS_create_button_methods**' is not executable in Python. It uses and must adhere to Python syntax, but it will be used in the browser, where it must be executable.")
st.markdown("It's the '**pscript**' module that translates Python into JavaScript. So when I say the method is 100% Python, it's true in principle, but the person writing the program must have some knowledge of JavaScript to debug it when the JavaScript doesn't do what it should.")
st.markdown("Without further ado, let's give an example of an 'Element Plus' button created for Streamlit using this method:")
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
st.markdown("The element that will be used by the end-user is the one listed on the last line of the program:")
st.code("Button = GenComponent('ElementPlusButton', create_button_template, genscript(JS_create_button_directives), genscript(JS_create_button_methods)).encapsulate(use_button)")
st.markdown("""
It's created by instantiating the GenComponent class, for which we pass 4 parameters:
1. a template
2. directives
3. methods
4. an encapsulation function
""")
st.markdown("###### Template")
st.code("""
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
""")
st.markdown("This is the part that generates the HTML tags needed to create the component on the page. In our example, we need a '**el-button**' tag. This is created by the '**gentag**' function. The generated elements sometimes have specific attributes that are not seen in standard HTML but are a Vue.js specificity. We have attributes prefixed with the '**:**' character like '**: disabled**'. This means the attribute references a directive that will be defined in the '**directives**' section. We also have attributes prefixed with the '**@**' character. These are attributes defined in the '**methods**' section. We have other attributes like '**v-if**' and '**v-else**' that allow conditionally generating HTML tags. The value of 'v-if' is a JavaScript expression that is either true or false. If it's true, the 'v-if' element will be used; otherwise, it's the 'v-else' element. Finally, for generating text outside attributes, there are elements like **{{label}}** in the example. They also reference definitions expressed in the 'directives' section.")
st.markdown("###### Directives")
st.code("""
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
""")
st.markdown("This is a function that returns a function whose output is a dictionary. The attribute ': disabled' is set to 'disabled'. The value of the attribute (disabled) should appear in the generated dictionary. In our case, we have ret['disabled'] = parameters.disabled. In other words, the disabled attribute of the el-button element will be set by the disabled parameter passed by Python.")
st.markdown("###### Methods")
st.code("""
def JS_create_button_methods(parameters):
    ret = dict()
    def fgetValue():
        Streamlit.setComponentValue(parameters.counter+1)
    ret['getValue'] = fgetValue
    return ret
""")
st.markdown("This is a function that returns a dictionary containing functions. The el-button element has been defined with the attribute @click=getValue. In other words, when the button is clicked, the 'getValue' method from the 'methods' section will be called. Typically, it's one of these methods that returns the output value to Python through the Streamlit.setComponentValue statement.")
st.markdown("Normally, a button returns a boolean value true or false. In our case, due to some side effect reasons, the button returns a counter that increments each time the button is pressed.")
st.markdown("###### Encapsulation function")
st.code("""
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
""")
st.markdown("""
The component created by GenComponent cannot be used as-is in the application for 2 reasons:
1. Input parameters must be specified and controlled within a class.
2. The functioning of Streamlit (automatic code rerun) introduces side effects related to how Streamlit reinstates components when input parameters are modified.
""")
st.markdown("Regarding the side effects on the button component, I've written an article that demonstrates the problem and the solution: https://reinstantiate-vraj6hsg8fpq66shvkugy5.streamlit.app/")
st.markdown("""
Ultimately, to create a Streamlit component xxxx, you simply need to define 4 functions:
1. create_xxxx_template
2. JS_create_xxxx_directives
3. JS_create_xxxx_methods
4. use_xxxx
""")
st.markdown("and assemble them with '**GenComponent**'")
st.markdown("All widgets created in this application are made this way.")
st.markdown("Of course, one must delve into the logic of Vue.js and consult the Element Plus documentation to be able to define a new widget.")
st.markdown(("And the method can be generalized to other environments than Element Plus and Vue.js (React, MUI, ...)."))