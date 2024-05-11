import streamlit as st, tempfile, os, json, pscript, inspect, yaml
import streamlit.components.v1 as components
from htmlgenerator import *
from streamlit_theme import st_theme
from streamlit_extras.switch_page_button import switch_page

def set_page_config():
    st.set_page_config(initial_sidebar_state='collapsed')
    st.markdown("""<style> [data-testid="collapsedControl"] {display: none}</style>""", unsafe_allow_html=True)
    theme = st_theme()
    return dict(streamlit_theme=theme['base']) if theme else dict(streamlit_theme='light')

def gen_back_button():
    if 'caller' in st.session_state and st.session_state.caller:
        c1, c2 = st.columns([8,1])
        with c2:
            if st.button('Back'): switch_page(st.session_state.caller)

def gentag(x):
    class C(HTMLElement):
        tag=x
    return C

def genvoid(x):
    class C(VoidElement):
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
            anchor = {}
            anchor.ElementPlus = ElementPlus
            anchor.state = {}
            console.log('parameters', parameters)
            if 'streamlit_theme' in parameters:
                html = document.querySelector("html")
                html.setAttribute("class", parameters.streamlit_theme)
            App = {}
            App.data = directives(parameters, anchor)
            App.methods = methods(parameters, anchor)
            app = Vue.createApp(App)
            app.use(ElementPlus)
            app.mount('#app')
            anchor.iframeHeight = parameters.height if hasattr(parameters, "height") else document.body.scrollHeight
            Streamlit.setFrameHeight(anchor.iframeHeight)
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
        head.append(STYLE('html.dark{color-scheme:dark;--el-color-primary:#409eff;--el-color-primary-light-3:#3375b9;--el-color-primary-light-5:#2a598a;--el-color-primary-light-7:#213d5b;--el-color-primary-light-8:#1d3043;--el-color-primary-light-9:#18222c;--el-color-primary-dark-2:#66b1ff;--el-color-success:#67c23a;--el-color-success-light-3:#4e8e2f;--el-color-success-light-5:#3e6b27;--el-color-success-light-7:#2d481f;--el-color-success-light-8:#25371c;--el-color-success-light-9:#1c2518;--el-color-success-dark-2:#85ce61;--el-color-warning:#e6a23c;--el-color-warning-light-3:#a77730;--el-color-warning-light-5:#7d5b28;--el-color-warning-light-7:#533f20;--el-color-warning-light-8:#3e301c;--el-color-warning-light-9:#292218;--el-color-warning-dark-2:#ebb563;--el-color-danger:#f56c6c;--el-color-danger-light-3:#b25252;--el-color-danger-light-5:#854040;--el-color-danger-light-7:#582e2e;--el-color-danger-light-8:#412626;--el-color-danger-light-9:#2b1d1d;--el-color-danger-dark-2:#f78989;--el-color-error:#f56c6c;--el-color-error-light-3:#b25252;--el-color-error-light-5:#854040;--el-color-error-light-7:#582e2e;--el-color-error-light-8:#412626;--el-color-error-light-9:#2b1d1d;--el-color-error-dark-2:#f78989;--el-color-info:#909399;--el-color-info-light-3:#6b6d71;--el-color-info-light-5:#525457;--el-color-info-light-7:#393a3c;--el-color-info-light-8:#2d2d2f;--el-color-info-light-9:#202121;--el-color-info-dark-2:#a6a9ad;--el-box-shadow:0px 12px 32px 4px rgba(0,0,0,0.36),0px 8px 20px rgba(0,0,0,0.72);--el-box-shadow-light:0px 0px 12px rgba(0,0,0,0.72);--el-box-shadow-lighter:0px 0px 6px rgba(0,0,0,0.72);--el-box-shadow-dark:0px 16px 48px 16px rgba(0,0,0,0.72),0px 12px 32px #000000,0px 8px 16px -8px #000000;--el-bg-color-page:#0a0a0a;--el-bg-color:#141414;--el-bg-color-overlay:#1d1e1f;--el-text-color-primary:#E5EAF3;--el-text-color-regular:#CFD3DC;--el-text-color-secondary:#A3A6AD;--el-text-color-placeholder:#8D9095;--el-text-color-disabled:#6C6E72;--el-border-color-darker:#636466;--el-border-color-dark:#58585B;--el-border-color:#4C4D4F;--el-border-color-light:#414243;--el-border-color-lighter:#363637;--el-border-color-extra-light:#2B2B2C;--el-fill-color-darker:#424243;--el-fill-color-dark:#39393A;--el-fill-color:#303030;--el-fill-color-light:#262727;--el-fill-color-lighter:#1D1D1D;--el-fill-color-extra-light:#191919;--el-fill-color-blank:transparent;--el-mask-color:rgba(0,0,0,0.8);--el-mask-color-extra-light:rgba(0,0,0,0.3)}html.dark .el-button{--el-button-disabled-text-color:rgba(255,255,255,0.5)}html.dark .el-card{--el-card-bg-color:var(--el-bg-color-overlay)}html.dark .el-empty{--el-empty-fill-color-0:var(--el-color-black);--el-empty-fill-color-1:#4b4b52;--el-empty-fill-color-2:#36383d;--el-empty-fill-color-3:#1e1e20;--el-empty-fill-color-4:#262629;--el-empty-fill-color-5:#202124;--el-empty-fill-color-6:#212224;--el-empty-fill-color-7:#1b1c1f;--el-empty-fill-color-8:#1c1d1f;--el-empty-fill-color-9:#18181a}'))
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

def JS_create_button_directives(parameters, anchor):
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
        ret['color'] = parameters.color
        ret['icon'] = Vue.shallowRef(ElementPlusIconsVue[parameters.icon])
        return ret
    return f

def JS_create_button_methods(parameters, anchor):
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
        options[':color'] = "color"
        options['@click'] = "getValue"
        ifoptions['v-if'] = "label !== null"
        elseoptions['v-else'] = True
        return DIV(ELBUTTON('{{label}}', **options, **ifoptions),ELBUTTON(**options, **elseoptions), id="app")

def use_button(component):
    class Component:
        def __init__(self, id=None, **d):
            id = f'Component_{id}'
            if id not in st.session_state: st.session_state[id] = dict(old=0, new=0)
            result = component(id=id, counter=st.session_state[id]['new'], default=st.session_state[id]['new'], **d)
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

def JS_create_button_group_directives(parameters, anchor):
    def f():
        def fbuttons():
            for b in range(len(parameters.buttons)):
                if hasattr(parameters.buttons[b], "icon"):
                    parameters.buttons[b].iconx = Vue.shallowRef(ElementPlusIconsVue[parameters.buttons[b].icon])
            return Vue.reactive(parameters.buttons)   
        ret = dict()
        ret['buttons'] = fbuttons()
        ret['type'] = parameters.type
        ret['size'] = parameters.size
        return ret
    return f

def JS_create_button_group_methods(parameters, anchor):
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
        def __init__(self, id=None, **d):
            id = f'Component_{id}'
            if id not in st.session_state: st.session_state[id] = dict(old=0, new=0)
            result = component(id=id, counter=st.session_state[id]['new'], **d)
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

def JS_create_checkbox_directives(parameters, anchor):
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

def JS_create_checkbox_methods(parameters, anchor):
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
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Checkbox = GenComponent('ElementPlusCheckbox', create_checkbox_template, genscript(JS_create_checkbox_directives), genscript(JS_create_checkbox_methods)).encapsulate(use_checkbox)

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

#####  Radio definition

def JS_create_radio_directives(parameters, anchor):
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

def JS_create_radio_methods(parameters, anchor):
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
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Radio = GenComponent('ElementPlusRadio', create_radio_template, genscript(JS_create_radio_directives), genscript(JS_create_radio_methods)).encapsulate(use_radio)

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

#####  Cascader definition

def JS_create_cascader_directives(parameters, anchor):
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

def JS_create_cascader_methods(parameters, anchor):
    ret = dict()
    def fhandleChange(x):
        Streamlit.setFrameHeight(anchor.iframeHeight) 
        result = []
        if x != undefined:
            result = JSON.parse(JSON.stringify(x))
        Streamlit.setComponentValue(result)    
    def fexpandchange(x):
        def f():
            Streamlit.setFrameHeight(document.body.scrollHeight)
        if x: setTimeout(f, 100)
        else: Streamlit.setFrameHeight(anchor.iframeHeight) 
    ret['handleChange'] = fhandleChange
    ret['expandchange'] = fexpandchange
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
        options['@visible-change'] = "expandchange"
        return DIV(ELCASCADER(**options), id="app")

def use_cascader(component):
    class Component:
        def __init__(self, default=[], **d):
            result = component(default=default, **d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Cascader = GenComponent('ElementPlusCascader', create_cascader_template, genscript(JS_create_cascader_directives), genscript(JS_create_cascader_methods)).encapsulate(use_cascader)


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

#####  DatePicker definition

def JS_create_date_picker_directives(parameters, anchor):
    def f():
        ret = dict()
        ret['value'] = Vue.ref('')
        ret['size'] = parameters.size
        ret['readonly'] = parameters.readonly
        ret['disabled'] = parameters.disabled
        ret['editable'] = parameters.editable
        ret['clearable'] = parameters.clearable
        ret['placeholder'] = parameters.placeholder
        ret['start_placeholder'] = parameters.start_placeholder
        ret['end_placeholder'] = parameters.end_placeholder
        ret['type'] = parameters.type
        ret['format'] = parameters.format
        ret['value_format'] = parameters.value_format
        return ret
    return f

def JS_create_date_picker_methods(parameters, anchor):
    ret = dict()
    def fsetdate(x):
        Streamlit.setComponentValue(JSON.parse(JSON.stringify(x)))
    def fvisiblechange(x):
        if x: Streamlit.setFrameHeight(document.body.scrollHeight) 
        else: Streamlit.setFrameHeight(anchor.iframeHeight)     
    ret['setDate'] = fsetdate
    ret["visiblechange"] = fvisiblechange   
    return ret

def create_date_picker_template():
        ELDATEPICKER = gentag("el-date-picker") 
        options = dict()
        options['v-model'] = "value"
        options[':size'] = "size"
        options[':readonly'] = "readonly"
        options[':disabled'] = "disabled"
        options[':editable'] = "editable"
        options[':clearable'] = "clearable"
        options[':placeholder'] = "placeholder"
        options[':start-placeholder'] = "start_placeholder"
        options[':end-placeholder'] = "end_placeholder"
        options[':type'] = "type"
        options[':format'] = "format"
        options[':value-format'] = "value_format"
        options['@change'] = "setDate"
        options['@visible-change'] = "visiblechange"
        return DIV(ELDATEPICKER(**options), id="app")

def use_date_picker(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

DatePicker = GenComponent('ElementPlusDatePicker', create_date_picker_template, genscript(JS_create_date_picker_directives), genscript(JS_create_date_picker_methods)).encapsulate(use_date_picker)

#####  Alert definition

def JS_create_alert_directives(parameters, anchor):
    def f():
        ret = dict()
        ret['title'] = parameters.title
        ret['type'] = parameters.type
        ret['description'] = parameters.description
        ret['closable'] = parameters.closable
        ret['center'] = parameters.center
        ret['effect'] = parameters.effect
        ret['show_icon'] = parameters.show_icon
        ret['close_alert'] = parameters.close_alert
        return ret
    return f

def JS_create_alert_methods(parameters, anchor):
    ret = dict()
    return ret

def create_alert_template():
        ELALERT = gentag("el-alert") 
        options = dict()
        options[':title'] = "title"
        options[':type'] = "type"
        options[':description'] = "description"
        options[':closable'] = "closable"
        options[':center'] = "center"
        options[':effect'] = "effect"
        options[':show-icon'] = "show_icon"
        options[':close-text'] = "close_text"
        return DIV(ELALERT(**options), id="app")

def use_alert(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Alert = GenComponent('ElementPlusAlert', create_alert_template, genscript(JS_create_alert_directives), genscript(JS_create_alert_methods)).encapsulate(use_alert)

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

#####  Slider definition

def JS_create_slider_directives(parameters, anchor):
    def f():
        ret = dict()
        ret["val"] = Vue.ref(parameters.value)
        ret["min"] = parameters.min
        ret["max"] = parameters.max
        ret["disabled"] = parameters.disabled
        ret["step"] = parameters.step
        ret["size"] = parameters.size
        ret["range"] = parameters.range
        ret["show_input"] = parameters.show_input
        ret["label"] = parameters.label
        ret["labelwidth"] = parameters.labelwidth
        ret["sliderwidth"] = parameters.sliderwidth
        return ret
    return f

def JS_create_slider_methods(parameters, anchor): 
    def fchange(x):
        Streamlit.setComponentValue(x) 
    ret = dict()
    ret["change"] = fchange    
    return ret

def create_slider_template():
        ELSLIDER = gentag("el-slider") 
        ELCOL = gentag("el-col") 
        ELROW = gentag("el-row") 
        options = dict()
        options['v-model'] = "val"
        options[':min'] = "min"
        options[':max'] = "max"
        options[':disabled'] = "disabled"
        options[':step'] = "step"
        options[':size'] = "size"
        options[':range'] = "range"
        options[':show-input'] = "show_input"
        options['@change'] = "change"
        loptions = dict()
        loptions[':span'] = "labelwidth"
        soptions = dict()
        soptions[':span'] = "sliderwidth"
        return DIV(ELROW(ELCOL(SPAN('{{label}}'),**loptions), ELCOL(ELSLIDER(**options), **soptions)), id="app")

def use_slider(component):
    class Component:
        def __init__(self, value=0, **d):
            result = component(value=value, default=value, **d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Slider = GenComponent('ElementPlusSlider', create_slider_template, genscript(JS_create_slider_directives), genscript(JS_create_slider_methods)).encapsulate(use_slider)

#####  TreeSelect definition

def JS_create_tree_select_directives(parameters, anchor):
    def f():
        ret = dict()
        ret["val"] = Vue.ref()
        ret["data"] = Vue.ref(parameters.data)
        ret["placeholder"] = parameters.placeholder
        ret["render_after_expand"] = parameters.render_after_expand
        ret["show_checkbox"] = parameters.show_checkbox
        ret["check_strictly"] = parameters.check_strictly
        ret["multiple"] = parameters.multiple
        ret["filterable"] = parameters.filterable
        ret["accordion"] = parameters.accordion
        return ret
    return f

def JS_create_tree_select_methods(parameters, anchor): 
    def fchange(x):
        Streamlit.setComponentValue(x)     
    def fvisiblechange(x):
        def f():
            Streamlit.setFrameHeight(document.body.scrollHeight)
        if x: setTimeout(f, 200)
        else: Streamlit.setFrameHeight(anchor.iframeHeight)     
    def fadjustspace(x):
        def f():
            Streamlit.setFrameHeight(document.body.scrollHeight)
        setTimeout(f, 200)
    ret = dict()
    ret["change"] = fchange    
    ret["visiblechange"] = fvisiblechange    
    ret["adjustspace"] = fadjustspace   
    return ret

def create_tree_select_template():
        ELTREESELECT = gentag("el-tree-select") 
        options = dict()
        options['v-model'] = "val"
        options[':data'] = "data"
        options[':placeholder'] = "placeholder"
        options[':render-after-expand'] = "render_after_expand"
        options[':show-checkbox'] = "show_checkbox"
        options[':check-strictly'] = "check_strictly"
        options[':multiple'] = "multiple"
        options[':filterable'] = "filterable"
        options[':accordion'] = "accordion"
        options['@change'] = "change"
        options['@visible-change'] = "visiblechange"
        options['@node-expand'] = "adjustspace"
        options['@node-collapse'] = "adjustspace"
        return DIV(ELTREESELECT(**options), id="app")

def use_tree_select(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

TreeSelect = GenComponent('ElementPlusTreeSelect', create_tree_select_template, genscript(JS_create_tree_select_directives), genscript(JS_create_tree_select_methods)).encapsulate(use_tree_select)

#####  Tree definition

def JS_create_tree_directives(parameters, anchor):
    def f():
        def fcustomnodeclass(data, node):
            console.log('node', node)
            console.log('data', data)
            if data._class:
                return data._class
            else: return None
        ret = dict()
        ret['customNodeClass'] = fcustomnodeclass
        ret["data"] = Vue.ref(parameters.data)
        ret["accordion"] = parameters.accordion
        ret["indent"] = parameters.indent
        ret["draggable"] = parameters.draggable
        ret['icon'] = Vue.shallowRef(ElementPlusIconsVue[parameters.icon])
        ret["expandonclick"] = parameters.expand_on_click_node
        ret["style"] = parameters.style
        return ret
    return f

def JS_create_tree_methods(parameters, anchor): 
    def fvisiblechange(x):
        def f():
            Streamlit.setFrameHeight(document.body.scrollHeight)
        if x: setTimeout(f, 200)
        else: Streamlit.setFrameHeight(anchor.iframeHeight)     
    def fadjustspace(x):
        def f():
            Streamlit.setFrameHeight(document.body.scrollHeight)
        setTimeout(f, 200)    
    def fselectnode(node):
        Streamlit.setComponentValue({'event':'click', 'id':node.id})
    def fhandleDragStart(node):
        Streamlit.setComponentValue({'event':'dragstart', 'label':node.data.id})
        console.log(node)
    def fhandleDragEnd(frm, to, type):
        Streamlit.setComponentValue({'event':'dragend', 'from':frm.data.id, 'to':to.data.id, 'where':type})
    def fhandleDrop(frm, to, type):
        console.log(frm)
        console.log(to)
        Streamlit.setComponentValue({'event':'drag&drop', 'from':frm.data.id, 'to':to.data.id, 'where':type})
    ret = dict()
    ret["visiblechange"] = fvisiblechange    
    ret["adjustspace"] = fadjustspace   
    ret["selectnode"] = fselectnode   
    ret["handleDragStart"] = fhandleDragStart   
    ret["handleDragEnd"] = fhandleDragEnd   
    ret["handleDrop"] = fhandleDrop   
    return ret

def create_tree_template():
        ELTREE = gentag("el-tree") 
        COMPONENT = gentag("component") 
        options = dict()
        options[':data'] = "data"
        options[':accordion'] = "accordion"
        options[':expand-on-click-node'] = "expandonclick"
        options[':indent'] = "indent"
        options[':icon'] = "icon"
        options[':props'] = "{ class: customNodeClass }"
        options[':draggable'] = "draggable"
        options['@node-click'] = "selectnode"
        options['@visible-change'] = "visiblechange"
        options['@node-expand'] = "adjustspace"
        options['@node-collapse'] = "adjustspace"
        options['@node-drag-start'] = "handleDragStart"
        options['@node-drag-end'] = "handleDragEnd"
        options['@node-drop'] = "handleDrop"
        coptions = dict()
        coptions[':is'] = "`style`"
        return DIV(COMPONENT('{{style}}', **coptions), ELTREE(**options), id="app")

def use_tree(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Tree = GenComponent('ElementPlusTree', create_tree_template, genscript(JS_create_tree_directives), genscript(JS_create_tree_methods)).encapsulate(use_tree)


#####  Result definition

def JS_create_result_directives(parameters, anchor):
    def f():
        ret = dict()
        ret["title"] = parameters.title
        ret['icon'] = parameters.icon
        ret["sub_title"] = parameters.description
        return ret
    return f

def JS_create_result_methods(parameters, anchor): 
    ret = dict()
    return ret

def create_result_template():
        ELRESULT = gentag("el-result") 
        options = dict()
        options[':title'] = "title"
        options[':icon'] = "icon"
        options[':sub-title'] = "sub_title"
        return DIV(ELRESULT(**options), id="app")

def use_result(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Result = GenComponent('ElementPlusResult', create_result_template, genscript(JS_create_result_directives), genscript(JS_create_result_methods)).encapsulate(use_result)

#####  Switch definition

def JS_create_switch_directives(parameters, anchor):
    def f():
        ret = dict()
        ret["val"] = parameters.value
        ret["size"] = parameters.size
        ret["width"] = parameters.width
        ret["disabled"] = parameters.disabled
        ret['aai'] = Vue.shallowRef(ElementPlusIconsVue[parameters.active_action_icon])
        ret['iai'] = Vue.shallowRef(ElementPlusIconsVue[parameters.inactive_action_icon])        
        ret["av"] = parameters.active_value
        ret["iv"] = parameters.inactive_value        
        ret["at"] = parameters.active_text
        ret["it"] = parameters.inactive_text
        ret["style"] = parameters.style
        return ret
    return f

def JS_create_switch_methods(parameters, anchor):
    def fchange(x):
        console.log(x)
        Streamlit.setComponentValue(x)
    ret = dict()
    ret["change"] = fchange    
    return ret

def create_switch_template():
        ELSWITCH = gentag("el-switch") 
        options = dict()
        options['v-model'] = "val"
        options[':size'] = "size"
        options[':width'] = "width"
        options[':disabled'] = "disabled"
        options[':active-action-icon'] = "aai"
        options[':inactive-action-icon'] = "iai"
        options[':active-value'] = "av"
        options[':inactive-value'] = "iv"
        options[':active-text'] = "at"
        options[':inactive-text'] = "it"
        options[':style'] = "style"
        options['@change'] = "change"
        return DIV(ELSWITCH(**options), id="app")

def use_switch(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Switch = GenComponent('ElementPlusSwitch', create_switch_template, genscript(JS_create_switch_directives), genscript(JS_create_switch_methods)).encapsulate(use_switch)

#####  Progress definition

def JS_create_progress_directives(parameters, anchor):
    def f():
        ret = dict()
        ret["percentage"] = parameters.percentage
        ret["status"] = parameters.status
        ret["type"] = parameters.type
        ret["stroke_width"] = parameters.stroke_width
        ret["text_inside"] = parameters.text_inside
        ret["color"] = parameters.color
        ret["striped"] = parameters.striped
        ret["striped_flow"] = parameters.striped_flow
        ret["duration"] = parameters.duration
        ret["indeterminate"] = parameters.indeterminate
        return ret
    return f

def JS_create_progress_methods(parameters, anchor):
    ret = dict()  
    return ret

def create_progress_template():
        ELPROGRESS = gentag("el-progress") 
        options = dict()
        options[':percentage'] = "percentage"
        options[':status'] = "status"
        options[':type'] = "type"
        options[':stroke-width'] = "stroke_width"
        options[':text-inside'] = "text_inside"
        options[':color'] = "color"
        options[':striped'] = "striped"
        options[':striped-flow'] = "striped_flow"
        options[':duration'] = "duration"
        options[':indeterminate'] = "indeterminate"
        return DIV(ELPROGRESS(**options), id="app")

def use_progress(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Progress = GenComponent('ElementPlusProgress', create_progress_template, genscript(JS_create_progress_directives), genscript(JS_create_progress_methods)).encapsulate(use_progress)

#####  BadgeButton definition

def JS_create_badge_button_directives(parameters, anchor):
    def f():
        ret = dict()
        ret['bvalue'] = parameters.badge_value
        ret['bmax'] = parameters.badge_max
        ret['bisdot'] = parameters.badge_is_dot
        ret['bhidden'] = parameters.badge_hidden
        ret['bcolor'] = parameters.badge_color
        ret['bshowzero'] = parameters.badge_show_zero
        ret['btype'] = parameters.badge_type
        ret['boffset'] = parameters.badge_offset
        ret['label'] = parameters.label
        ret['link'] = parameters.link
        ret['type'] = parameters.type
        ret['size'] = parameters.size
        ret['round'] = parameters.round
        ret['plain'] = parameters.plain
        ret['disabled'] = parameters.disabled
        ret['circle'] = parameters.circle
        ret['color'] = parameters.color
        ret['icon'] = Vue.shallowRef(ElementPlusIconsVue[parameters.icon])
        return ret
    return f

def JS_create_badge_button_methods(parameters, anchor):
    ret = dict()
    def fgetValue():
        Streamlit.setComponentValue(parameters.counter+1)    
    ret['getValue'] = fgetValue
    return ret

def create_badge_button_template():
        ELBADGE = gentag("el-badge")
        ELBUTTON = gentag("el-button")
        boptions = dict()
        boptions[':value'] = "bvalue"
        boptions[':max'] = "bmax"
        boptions[':is-dot'] = "bisdot"
        boptions[':hidden'] = "bhidden"
        boptions[':color'] = "bcolor"
        boptions[':show-zero'] = "bshowzero"
        boptions[':type'] = "btype"
        boptions[':offset'] = "boffset"
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
        options[':color'] = "color"
        options['@click'] = "getValue"
        ifoptions['v-if'] = "label !== null"
        elseoptions['v-else'] = True
        return DIV(ELBADGE(ELBUTTON('{{label}}', **options, **ifoptions),ELBUTTON(**options, **elseoptions), **boptions), id="app")

def use_badge_button(component):
    class Component:
        def __init__(self, id=None, **d):
            id = f'Component_{id}'
            if id not in st.session_state: st.session_state[id] = dict(old=0, new=0)
            result = component(id=id, counter=st.session_state[id]['new'], default=st.session_state[id]['new'], **d)
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

BadgeButton = GenComponent('ElementPlusBadgeButton', create_badge_button_template, genscript(JS_create_badge_button_directives), genscript(JS_create_badge_button_methods)).encapsulate(use_badge_button)

#####  Menu definition

def JS_create_menu_directives(parameters, anchor):
    def f():
        ret = dict()
        ret['activeIndex'] = parameters.active_index
        ret['mode'] = parameters.mode
        ret['items'] = parameters.items
        ret['bgcolor'] = parameters.background_color
        ret['txtcolor'] = parameters.text_color
        ret['actxtcolor'] = parameters.active_text_color
        ret['ellipsis'] = parameters.ellipsis
        return ret
    return f

def JS_create_menu_methods(parameters, anchor):
    def fselect(x):
        Streamlit.setComponentValue(x)    
    def fopen(x):
        def f():
            Streamlit.setFrameHeight(document.body.scrollHeight)
        if x: setTimeout(f, 200)
        else: Streamlit.setFrameHeight(anchor.iframeHeight) 
    def fclose(x):
        Streamlit.setFrameHeight(anchor.iframeHeight) 
    ret = dict()
    ret['select'] = fselect
    ret['open'] = fopen
    ret['close'] = fclose
    return ret

def create_menu_template():
        ELMENU = gentag("el-menu")
        ELSUBMENU = gentag("el-sub-menu")
        ELMENUITEM = gentag("el-menu-item")
        TEMPLATE = gentag("template")
        toptions= dict()
        toptions['v-for'] = "item in items"
        ioptions = dict()
        ioptions[':index'] = "item.index"
        ioptions[':disabled'] = "item.disabled"
        ioptions['v-if'] = "item.type === 'item'"
        soptions = dict()
        soptions['v-else'] = True
        soptions[':index'] = "item.index"
        xoptions = dict()
        xoptions['#title'] = True
        joptions = dict()
        joptions['v-for'] = "subitem in item.items"
        joptions[':index'] = "subitem.index"
        joptions[':disabled'] = "subitem.disabled"
        options=dict()
        options[':default-active'] = "activeIndex"
        options[':mode'] = "mode"
        options[':ellipsis'] = "ellipsis"
        options[':background-color'] = "bgcolor"
        options[':text-color'] = "txtcolor"
        options[':active-text-color'] = "actxtcolor"
        options['@select'] = "select"
        options['@open'] = "open"
        options['@close'] = "close"
        return DIV(ELMENU(TEMPLATE(ELMENUITEM('{{item.label}}', **ioptions), ELSUBMENU(TEMPLATE('{{item.label}}', **xoptions), ELMENUITEM('{{subitem.label}}', **joptions), **soptions), **toptions), **options), id="app")

def use_menu(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

Menu = GenComponent('ElementPlusMenu', create_menu_template, genscript(JS_create_menu_directives), genscript(JS_create_menu_methods)).encapsulate(use_menu)
