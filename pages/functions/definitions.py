import streamlit as st, tempfile, os, json, pscript, inspect
import streamlit.components.v1 as components
from htmlgenerator import *
from streamlit_extras.switch_page_button import switch_page


def set_page_config():
    st.set_page_config(initial_sidebar_state='collapsed')
    st.markdown("""<style> [data-testid="collapsedControl"] {display: none}</style>""", unsafe_allow_html=True)

def gen_back_button():
    if 'caller' in st.session_state and st.session_state.caller:
        c1, c2 = st.columns([8,1])
        with c2:
            if st.button('Back'): switch_page(st.session_state.caller)

def gentag(x):
    class C(HTMLElement):
        tag=x
    return C

def genscript(f):
    source = pscript.py2js(inspect.getsource(f))
    name = f.__name__
    return dict(name=name, source=source)

def showcodeandrun(bloc):
    st.code(bloc)
    compiled_code = compile(bloc, "<string>", "exec")
    exec(compiled_code)
    st.divider()

def include(x, y):
    y.append(x)
    return x

class Container:
    def __init__(self, *x):
        self.children = []
        for e in x: self.children.append(e)
    def append(self, x):
        self.children.append(x)
    def __repr__(self):
        result = mark_safe('\n'.join([repr(e) if isinstance(e, Container) else e for e in self.children]))
        return result

def JS_header():
    def sendMessageToStreamlitClient(type, data):
        outData = Object.assign(dict(isStreamlitMessage=True, type=type), data)
        window.parent.postMessage(outData, "*")

    def setCR():
        sendMessageToStreamlitClient("streamlit:componentReady", dict(apiVersion=1))

    def setCV(value):
        sendMessageToStreamlitClient("streamlit:setComponentValue", dict(value=value))

    def setFH(height):
        sendMessageToStreamlitClient("streamlit:setFrameHeight", dict(height=height))

    def addEL(type, callback):
        def f(event):
            if event.data.type == type:
                callback(event)
        window.addEventListener("message",f)
    return dict(setComponentReady=setCR, setComponentValue=setCV, setFrameHeight=setFH, events=dict(addEventListener=addEL))

HEADERSCRIPT = genscript(JS_header)

def JS_body(directives, methods):
    def onRender(event):
        if not window.rendered:
            parameters = event.data.args
            parameters.xxxstatexxx = {}
            console.log('parameters', parameters)
            console.log('directives', directives(parameters)())
            console.log('methods', methods(parameters))
            App = {}
            App.data = directives(parameters)
            App.methods = methods(parameters)
            console.log('App', App)
            app = Vue.createApp(App)
            app.use(ElementPlus)
            app.mount('#app')
            if hasattr(parameters, "height"): Streamlit.setFrameHeight(parameters.height)
            else: Streamlit.setFrameHeight(document.body.scrollHeight)
            window.rendered = True
    Streamlit.events.addEventListener("streamlit:render", onRender)
    Streamlit.setComponentReady()

BODYSCRIPT = genscript(JS_body)

class GenPage:
    def __init__(self, template, directives, methods):
        html = HTML()
        head = include(HEAD(), html)
        head.append(SCRIPT(src="https://unpkg.com/vue@3"))
        head.append(SCRIPT(src="https://unpkg.com/@element-plus/icons-vue"))
        head.append(LINK(rel="stylesheet",href="https://unpkg.com/element-plus/dist/index.css"))
        head.append(SCRIPT(src="https://unpkg.com/element-plus"))
        source = f'{HEADERSCRIPT["source"]}\nStreamlit={HEADERSCRIPT["name"]}();'
        head.append(SCRIPT(mark_safe(source)))
        body = include(BODY(), html)
        body.append(template())
        source = f'{directives["source"]}\n{methods["source"]}\n{BODYSCRIPT["source"]}\n{BODYSCRIPT["name"]}({directives["name"]}, {methods["name"]})'
        body.append(SCRIPT(mark_safe(source)))
        self.html = html
    def render(self, file=None):
        f =open(file, 'w')
        f.write('\n'.join([e for e in self.html.render(None)]))
        f.close()
    def gencomponent(self, name):
        dir = f"{tempfile.gettempdir()}/{name}"
        if not os.path.isdir(dir): os.mkdir(dir)
        fname = f'{dir}/index.html'
        print(fname)
        self.render(fname)
        func = components.declare_component(name, path=str(dir))
        def f(**params):
            component_value = func(**params)
            return component_value
        return f

class GenComponent:
    def __init__(self, name, template, directives, methods):
        self.component = GenPage(template, directives, methods).gencomponent(name)
    def encapsulate(self, use):
        return use(self.component)

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

#####  ButtonGroup definition

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

#####  Checkbox definition

def JS_create_checkbox_directives(parameters):
    def f():
        def fcheckboxes():
            for b in range(len(parameters.checkboxes)): parameters.xxxstatexxx[parameters.checkboxes[b].id] = parameters.checkboxes[b]
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

def JS_create_checkbox_methods(parameters):
    ret = dict()
    def fhandleItem(checkbox):
        result = dict()
        for b in parameters.xxxstatexxx:
            if parameters.xxxstatexxx[b].id == checkbox.id:
                if parameters.xxxstatexxx[b].val == parameters.xxxstatexxx[b].truevalue: parameters.xxxstatexxx[b].val = parameters.xxxstatexxx[b].falsevalue
                else: parameters.xxxstatexxx[b].val = parameters.xxxstatexxx[b].truevalue
            result[b] = parameters.xxxstatexxx[b].val
        Streamlit.setComponentValue(result)
    ret['handleItem'] = fhandleItem
    return ret


def create_checkbox_template():
        ELCHECKBOX = gentag("el-checkbox")
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
        return DIV(ELCHECKBOXGROUP(ELCHECKBOX(**coptions), **goptions), id="app")

def use_checkbox(component):
    class Component:
        def __init__(self, checkboxes=[], size='default', key=None, label=None, default=None, fill=None, min=None, max=None, disabled=False, textcolor=None):
            result = component(checkboxes=checkboxes, size=size, label=label, fill=fill, min=min, max=max, disabled=disabled, textcolor=textcolor, key=key, default=default)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Checkbox = GenComponent('ElementPlusCheckbox', create_checkbox_template, genscript(JS_create_checkbox_directives), genscript(JS_create_checkbox_methods)).encapsulate(use_checkbox)

#####  CheckboxButton definition

def JS_create_checkbox_button_directives(parameters):
    def f():
        def fcheckboxes():
            for b in range(len(parameters.checkboxes)): parameters.xxxstatexxx[parameters.checkboxes[b].id] = parameters.checkboxes[b]
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

def JS_create_checkbox_button_methods(parameters):
    ret = dict()
    def fhandleItem(checkbox):
        result = dict()
        for b in parameters.xxxstatexxx:
            if parameters.xxxstatexxx[b].id == checkbox.id:
                if parameters.xxxstatexxx[b].val == parameters.xxxstatexxx[b].truevalue: parameters.xxxstatexxx[b].val = parameters.xxxstatexxx[b].falsevalue
                else: parameters.xxxstatexxx[b].val = parameters.xxxstatexxx[b].truevalue
            result[b] = parameters.xxxstatexxx[b].val
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
        def __init__(self, checkboxes=[], size='default', key=None, label=None, default=None, fill=None, min=None, max=None, disabled=False, textcolor=None):
            result = component(checkboxes=checkboxes, size=size, label=label, fill=fill, min=min, max=max, disabled=disabled, textcolor=textcolor, key=key, default=default)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

CheckboxButton = GenComponent('ElementPlusCheckboxButton', create_checkbox_button_template, genscript(JS_create_checkbox_button_directives), genscript(JS_create_checkbox_button_methods)).encapsulate(use_checkbox_button)

#####  Radio definition

def JS_create_radio_directives(parameters):
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

def JS_create_radio_methods(parameters):
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
        def __init__(self, buttons=[], size='default', key=None, default=None, fill=None, disabled=False, textcolor=None):
            result = component(buttons=buttons, size=size, fill=fill, disabled=disabled, textcolor=textcolor, key=key, default=default)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Radio = GenComponent('ElementPlusRadio', create_radio_template, genscript(JS_create_radio_directives), genscript(JS_create_radio_methods)).encapsulate(use_radio)

#####  RadioButton definition

def JS_create_radio_button_directives(parameters):
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

def JS_create_radio_button_methods(parameters):
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
        def __init__(self, buttons=[], size='default', key=None, default=None, fill=None, disabled=False, textcolor=None):
            result = component(buttons=buttons, size=size, fill=fill, disabled=disabled, textcolor=textcolor, key=key, default=default)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

RadioButton = GenComponent('ElementPlusRadioButton', create_radio_button_template, genscript(JS_create_radio_button_directives), genscript(JS_create_radio_button_methods)).encapsulate(use_radio_button)

#####  Cascader definition

def JS_create_cascader_directives(parameters):
    def f():
        ret = dict()
        ret['options'] = parameters.options
        ret['model'] = Vue.ref([])
        ret['props'] = parameters.props
        ret['size'] = parameters.size
        ret['filterable'] = parameters.filterable
        ret['clearable'] = parameters.clearable
        return ret
    return f

def JS_create_cascader_methods(parameters):
    ret = dict()
    def fhandleChange(x):
        result = []
        if x != undefined:
            result = JSON.parse(JSON.stringify(x))
        Streamlit.setComponentValue(result)
    ret['handleChange'] = fhandleChange
    return ret

def create_cascader_template():
        ELCASCADER = gentag("el-cascader")
        options = dict()
        options['v-model'] = "model"
        options[':options'] = "options"
        options[':props'] = "props"
        options[':size'] = "size"
        options[':filterable'] = "filterable"
        options[':clearable'] = "clearable"
        options['@change'] = "handleChange"
        return DIV(ELCASCADER(**options), id="app")

def use_cascader(component):
    class Component:
        def __init__(self, options=[], props={}, filterable=True, clearable=True, size=None, height=None, key=None, default=[]):
            result = component(options=options, props=props, size=size, filterable=filterable, clearable=clearable, height=height, key=key, default=default)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Cascader = GenComponent('ElementPlusCascader', create_cascader_template, genscript(JS_create_cascader_directives), genscript(JS_create_cascader_methods)).encapsulate(use_cascader)


#####  Tag definition

def JS_create_tag_directives(parameters):
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

def JS_create_tag_methods(parameters):
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
        def __init__(self, tags=[], round=False, size='default', effect='light', closable=True, editable=False, label=None, space=10, key=None, default=[]):
            result = component(tags=tags, round=round, size=size, effect=effect, closable=closable, editable=editable, label=label, space=space, key=key, default=default)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Tag = GenComponent('ElementPlusTag', create_tag_template, genscript(JS_create_tag_directives), genscript(JS_create_tag_methods)).encapsulate(use_tag)
