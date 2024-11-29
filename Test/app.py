import sys
import os

# Get the parent directory (where pype.py is located)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


import pype
from pype import HTMLAttributes

prevCount = 0

def updatingFunc(app):
    #this function runs on a background thread
    pass

def changed_count(app):
    global prevCount

    count = app.state["count"]

    if(count > prevCount):
        app.instantiate("prefab-number",f"number-${count}","prefab-parent",[count])
    elif(count < prevCount):
        app.destroy("prefab-number",f"number-${prevCount}")

    prevCount = count
    print(f'\033[102m Pype \033[0m Count changed to: {count}')

app = pype.Pype("Testing",tools=False)
app.set_state("count",0)
app.bind('count','count',HTMLAttributes.INNERHTML)
app.hook('count',changed_count)
app.run([updatingFunc])