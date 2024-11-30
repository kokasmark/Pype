import webview
import threading
import os
import sys
import json
import copy

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
    def __init__(self, title="Pype Application", entry="./frontend/", width=900, height = 600,tools = True):
        """Initialize the App"""
        os.system("")

        self.state = {"title": title}
        self.previous_state = {"title": title}

        self.nodes = {}  # Stores node relationships
        self.hooks = {}  # Stores hooks that are called on a specific state change
        self.observers = {} # Stores observers, each observer observes a state array, where prefab attributes are stored. Manages prefabs.
        self.exposed = {} # Functions that are exposed to the app

        self.config = {"title": title, "entry": entry, "tools": tools, "width": width, "height":height}
        self.running = False

    def update(self):
        """Run background tasks periodically."""

        if self.running:
            for function in self.functions:
                try:
                    function(self)
                except Exception as e:
                    self.log(str(e),'error')
                    
        threading.Timer(0, self.update).start() 

    def run(self, functions=[], pages=["index.html"]):
        """Start the app and background tasks."""

        self.log('is running!')
        self.functions = functions
        self.pages = pages

        self.update()
        
        self._window = webview.create_window(title=self.config["title"], url=self.config["entry"]+'index.html', js_api=self,width=self.config["width"],height=self.config["height"])
        self.running = True
        webview.start(debug=self.config["tools"],gui='edgechromium')

    def load_page(self, index):
        """Loads a page from the exposed pages, the unloaded page gets .unloaded for exit animations, and .loaded for the loaded for entry animations"""
        self._window.evaluate_js(f"unload({index})")# Pass the next page index to the unload so it can call load_page_immidiate after exit animations

    def load_page_immidiate(self,index):
        self._window.load_url(self.pages[index])

    def expose(self, function):
        """Exposes a function from the app side"""
        self.exposed[function.__name__] = function

    def call(self,name):
        """Calls a function from the app side"""
        self.exposed[name](self)

    def set_state(self, key, value):
        """Sets a state value and updates any nodes binded to it"""
        self.state[key] = value

        if key in self.observers:
            self.handle_observer(self.observers[key])
            
        if key in self.hooks:
            try:
                self.hooks[key](self)  # Call the hook function
            except Exception as e:
                self.log(str(e),"error")

        if self.running:
            self.update_frontend(key, value)  
        
        self.previous_state[key] = value

    def get_state(self, key):
        """Returns a state value"""
        value = self.state.get(key, None)
        if value is None:
            return None
        else:
            return copy.deepcopy(value)
    
    def get_prev_state(self, key):
        """Returns a state value"""
        value = self.previous_state.get(key, None)
        if value is None:
            return None
        else:
            return copy.deepcopy(value) 
    
    def init_frontend(self):
        """Renders the frontend with the initial state values"""

        for key in self.state.keys():
            self.update_frontend(key,self.state[key])
        return self.state
    
    def bind(self, node_id, state_key, attr=HTMLAttributes.INNERHTML):
        """Binds a node to a state value"""
        self.nodes[state_key] = {"id": node_id, "attribute": attr.value}
        self.log(f'Nodes with key: \033[1m{node_id}\033[0m will render state: \033[1m{state_key}\033[0m with attribute: \033[1m{attr.value}\033[0m')

    def hook(self, state_key, function):
        self.hooks[state_key] = function
        self.log(f'Hooked \033[1m{function.__name__}()\033[0m to state \033[1m{state_key}\033[0m')

    def observe(self, state_key, prefab_id, key_prefix, parent_id):
        """Observes the changes in a state array where the elements are attributes for a prefab"""
        """Handles instantiation and destroying based on the array size and content"""

        self.observers[state_key] = {"prefab_id": prefab_id, "key_prefix": key_prefix, "parent_id": parent_id, "attributes": state_key}
        self.log(f"\033[1m{state_key}\033[0m is observed, rendering prefab \033[1m{prefab_id}\033[0m")

    def handle_observer(self, observer):
        attributes_array = self.state[observer["attributes"]]
        prev_attributes_array = self.previous_state[observer["attributes"]]

        delta = len(attributes_array) - len(prev_attributes_array)

        if delta > 0:
            self.instantiate(observer["prefab_id"],f'{observer["key_prefix"]}-{len(attributes_array)}',observer["parent_id"],attributes_array[len(attributes_array)-1])
        if delta < 0:
            self.destroy(observer["prefab_id"], f'{observer["key_prefix"]}-{len(prev_attributes_array)}')

        pass

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
        observer = self.observers.get(key)
        if (node is None) and (observer is None):
            self.log(f'Warning {key} doesnt have a binded UI element!','warning')
            return
        if self._window != None and not (node is None):
            self._window.evaluate_js(f'updateElement("{node["id"]}","{node["attribute"]}", "{value}")')
