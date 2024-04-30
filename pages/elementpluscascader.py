import streamlit as st
from pages.functions.definitions import *
from streamlit_extras.switch_page_button import switch_page

set_page_config()
gen_back_button()

st.subheader("Cascader", divider="rainbow")
options = [
  {
    'value': 'guide',
    'label': 'Guide',
    'disabled': True,
    'children': [
      {
        'value': 'disciplines',
        'label': 'Disciplines',
        'children': [
          {
            'value': 'consistency',
            'label': 'Consistency',
          },
          {
            'value': 'feedback',
            'label': 'Feedback',
          },
          {
            'value': 'efficiency',
            'label': 'Efficiency',
          },
          {
            'value': 'controllability',
            'label': 'Controllability',
          },
        ],
      },
      {
        'value': 'navigation',
        'label': 'Navigation',
        'children': [
          {
            'value': 'side nav',
            'label': 'Side Navigation',
          },
          {
            'value': 'top nav',
            'label': 'Top Navigation',
          },
        ],
      },
    ],
  },
  {
    'value': 'component',
    'label': 'Component',
    'children': [
      {
        'value': 'basic',
        'label': 'Basic',
        'children': [
          {
            'value': 'layout',
            'label': 'Layout',
          },
          {
            'value': 'color',
            'label': 'Color',
          },
          {
            'value': 'typography',
            'label': 'Typography',
          },
          {
            'value': 'icon',
            'label': 'Icon',
          },
          {
            'value': 'button',
            'label': 'Button',
          },
        ],
      },
      {
        'value': 'form',
        'label': 'Form',
        'children': [
          {
            'value': 'radio',
            'label': 'Radio',
          },
          {
            'value': 'checkbox',
            'label': 'Checkbox',
          },
          {
            'value': 'input',
            'label': 'Input',
          },
          {
            'value': 'input-number',
            'label': 'InputNumber',
          },
          {
            'value': 'select',
            'label': 'Select',
          },
          {
            'value': 'cascader',
            'label': 'Cascader',
          },
          {
            'value': 'switch',
            'label': 'Switch',
          },
          {
            'value': 'slider',
            'label': 'Slider',
          },
          {
            'value': 'time-picker',
            'label': 'TimePicker',
          },
          {
            'value': 'date-picker',
            'label': 'DatePicker',
          },
          {
            'value': 'datetime-picker',
            'label': 'DateTimePicker',
          },
          {
            'value': 'upload',
            'label': 'Upload',
          },
          {
            'value': 'rate',
            'label': 'Rate',
          },
          {
            'value': 'form',
            'label': 'Form',
          },
        ],
      },
      {
        'value': 'data',
        'label': 'Data',
        'children': [
          {
            'value': 'table',
            'label': 'Table',
          },
          {
            'value': 'tag',
            'label': 'Tag',
          },
          {
            'value': 'progress',
            'label': 'Progress',
          },
          {
            'value': 'tree',
            'label': 'Tree',
          },
          {
            'value': 'pagination',
            'label': 'Pagination',
          },
          {
            'value': 'badge',
            'label': 'Badge',
          },
        ],
      },
      {
        'value': 'notice',
        'label': 'Notice',
        'children': [
          {
            'value': 'alert',
            'label': 'Alert',
          },
          {
            'value': 'loading',
            'label': 'Loading',
          },
          {
            'value': 'message',
            'label': 'Message',
          },
          {
            'value': 'message-box',
            'label': 'MessageBox',
          },
          {
            'value': 'notification',
            'label': 'Notification',
          },
        ],
      },
      {
        'value': 'navigation',
        'label': 'Navigation',
        'children': [
          {
            'value': 'menu',
            'label': 'Menu',
          },
          {
            'value': 'tabs',
            'label': 'Tabs',
          },
          {
            'value': 'breadcrumb',
            'label': 'Breadcrumb',
          },
          {
            'value': 'dropdown',
            'label': 'Dropdown',
          },
          {
            'value': 'steps',
            'label': 'Steps',
          },
        ],
      },
      {
        'value': 'others',
        'label': 'Others',
        'children': [
          {
            'value': 'dialog',
            'label': 'Dialog',
          },
          {
            'value': 'tooltip',
            'label': 'Tooltip',
          },
          {
            'value': 'popover',
            'label': 'Popover',
          },
          {
            'value': 'card',
            'label': 'Card',
          },
          {
            'value': 'carousel',
            'label': 'Carousel',
          },
          {
            'value': 'collapse',
            'label': 'Collapse',
          },
        ],
      },
    ],
  },
  {
    'value': 'resource',
    'label': 'Resource',
    'children': [
      {
        'value': 'axure',
        'label': 'Axure Components',
      },
      {
        'value': 'sketch',
        'label': 'Sketch Templates',
      },
      {
        'value': 'docs',
        'label': 'Design Documentation',
      },
    ],
  },
]
props = dict(expandTrigger="hover", multiple=True)
cas1 = Cascader(options=options, props=props, size='large', height=300)
st.write(cas1.get())
st.divider()
st.markdown("###### The code used to create the Cascader component")
st.code("""
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

Cascader = GenComponent('ElementPlusCascader', create_cascader_template, genscript(JS_create_cascader_directives), genscript(JS_create_cascader_methods)).encapsulate(use_cascader
""")
