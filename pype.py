import webview
import threading
import os
import sys
import json

from enum import Enum

class HTMLAttributes(Enum):
    # Common attributes
    CLASS = 'class'
    ID = 'id'
    STYLE = 'style'
    INNERHTML = 'innerHTML'
    TITLE = 'title'
    ALT = 'alt'
    HREF = 'href'
    SRC = 'src'
    ACTION = 'action'
    METHOD = 'method'
    TARGET = 'target'
    REL = 'rel'
    TYPE = 'type'
    VALUE = 'value'
    NAME = 'name'
    PLACEHOLDER = 'placeholder'
    REQUIRED = 'required'
    DISABLED = 'disabled'
    READONLY = 'readonly'
    CHECKED = 'checked'
    MAX = 'max'
    MIN = 'min'
    PATTERN = 'pattern'
    STEP = 'step'
    AUTOCOMPLETE = 'autocomplete'
    AUTOFOCUS = 'autofocus'
    MULTIPLE = 'multiple'
    ACCEPT = 'accept'
    COLSPAN = 'colspan'
    ROWSPAN = 'rowspan'
    LANG = 'lang'
    DIR = 'dir'
    ONCLICK = 'onclick'
    ONCHANGE = 'onchange'
    ONLOAD = 'onload'
    ONMOUSEOVER = 'onmouseover'
    ONMOUSEOUT = 'onmouseout'
    ONKEYDOWN = 'onkeydown'
    ONKEYUP = 'onkeyup'
    ONFOCUS = 'onfocus'
    ONBLUR = 'onblur'

class Pype:
    def __init__(self, title="Pype Application", entry="./frontend/", tools = True):
        """Initialize the App"""
        os.system("")

        self.state = {"title": title}
        self.nodes = {}  # Stores node relationships
        self.hooks = {}  # Stores hooks that are called on a specific state change
        self.config = {"title": title, "entry": entry, "tools": tools}
        self.running = False

    def update(self):
        """Run background tasks periodically."""

        for function in self.functions:
            try:
                function(self)
            except Exception as e:
                self.log(str(e),'error')
        if self.running:
            threading.Timer(0, self.update).start() 

    def run(self, functions=[]):
        """Start the app and background tasks."""

        self.log(' is running!')
        self.running = True
        self.functions = functions

        self.update()

        self._window = webview.create_window(title=self.config["title"], url=self.config["entry"]+'index.html', js_api=self)

        webview.start(debug=self.config["tools"],gui='edgechromium')

    def set_state(self, key, value):
        """Sets a state value and updates any nodes binded to it"""

        self.state[key] = value

        if key not in self.hooks:
            self.hooks[key] = None #Set a None hook

        if self.hooks[key] is not None:
            try:
                self.hooks[key](self)  # Call the hook function
            except Exception as e:
                self.log(str(e),"error")

        if self.running:
            self.update_frontend(key, value)  
    
    def get_state(self, key):
        """Returns a state value"""

        return self.state.get(key, None)
    
    def init_frontend(self):
        """Renders the frontend with the initial state values"""

        for key in self.state.keys():
            self.update_frontend(key,self.state[key])
        return self.state
    
    # Stores node relationships
    def bind(self, node_id, state_key, attr=HTMLAttributes.INNERHTML):
        """Binds a node to a state value"""
        self.nodes[state_key] = {"id": node_id, "attribute": attr.value}
        self.log(f'Node with id: \033[1m{node_id}\033[0m will render state: \033[1m{state_key}\033[0m with attribute: \033[1m{attr.value}\033[0m')

    def hook(self, state_key, function):
        self.hooks[state_key] = function
        self.log(f'Hooked \033[1m{function.__name__}()\033[0m to state \033[1m{state_key}\033[0m')

    def error(self,error_message):
        if self._window != None:
            self._window.evaluate_js(f'error("An error has occured: {error_message}",true)')
        self.log(f'An error has occured: {error_message}','error')

    def instantiate(self,prefab_id,key,parent,attr):
        """Copies and Instantiates a prefab from the html, setting its parent and attributes in order"""
        """With the attributes you can give its children ids so they react to state changes"""
        attr_json = json.dumps(attr)
        if self._window != None:
            self._window.evaluate_js(f'instantiate("{prefab_id}","{key}","{parent}", {attr_json})')

    def destroy(self,prefab_id,key):
        """Destroys an instantiated prefab"""
        if self._window != None:
            self._window.evaluate_js(f'destroy("{prefab_id}","{key}")')
    
    def log(self,message,type='success'):
        header = f'\033[42m Pype \033[0m'

        if type == 'warning':
            header = f'\033[43m Pype \033[0m'
        if type == 'error':
            header = f'\033[41m Pype \033[0m'
            self.error(message)

        print(f'{header} {message}')

    def update_frontend(self, key, value):
        node = self.nodes.get(key)
        if node == None:
            self.log(f'Warning {key} doesnt have a binded UI element!','warning')
            return
        if self._window != None:
            self._window.evaluate_js(f'updateElement("{node["id"]}","{node["attribute"]}", "{value}")')
