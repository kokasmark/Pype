import webview
import threading

class Pype:
    def __init__(self, title="Pype Application", entry="./frontend/index.html", build="dev"):
        """Initialize the App"""

        self.state = {"title": title}
        self.nodes = {}  # Stores node relationships
        self.config = {"title": title, "entry": entry, "build": build}
        self.running = False

    def update(self):
        """Run background tasks periodically."""

        for function in self.functions:
            function(self)
        if self.running:
            threading.Timer(0, self.update).start() 

    def run(self, functions=[]):
        """Start the app and background tasks."""

        print('\33[102m' + ' Pype ' + '\33[0m'+' is running!')
        self.running = True
        self.functions = functions

        self.update()

        self._window = webview.create_window(title=self.config["title"], url=self.config["entry"], js_api=self)

        webview.start(debug=(self.config["build"] == "dev"))

    def set_state(self, key, value):
        """Sets a state value and updates any nodes binded to it"""

        self.state[key] = value
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
    def bind(self, node_id, state_key):
        """Binds a node to a state value"""

        self.nodes[state_key] = node_id
        print(f"Node with id: {node_id} will render state.{state_key}")
    
    def update_frontend(self, key, value):
        if self._window != None:
            self._window.evaluate_js(f'updateElement("{self.nodes.get(key)}", "{value}")')
