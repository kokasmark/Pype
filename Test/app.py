import sys
import os

# Get the parent directory (where pype.py is located)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


import pype
from pype import HTMLAttributes
import random

prevCount = 0
def updatingFunc(app):
    #this function runs on a background thread
    pass

def changed_count(app):
    global prevCount

    count = app.state["count"]

    if(count > prevCount):
        random_color = f'rgb({random.randint(50,255)},{random.randint(50,255)},{random.randint(50,255)})'
        app.instantiate("prefab-number",f"number-${count}","prefab-parent",{"count":count, "color": random_color})
    elif(count < prevCount):
        app.destroy("prefab-number",f"number-${prevCount}")

    prevCount = count
    app.log(f'Count changed to: {count}')

app = pype.Pype("Testing",tools=False)
app.set_state("count",0)
app.bind('count','count',HTMLAttributes.INNERHTML)
app.hook('count',changed_count)
app.run([updatingFunc])