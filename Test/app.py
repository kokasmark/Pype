import sys
import os

# Get the parent directory (where pype.py is located)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


import pype
from pype import HTMLAttributes
import random
import numpy as np

def generateImage(app):
    #this function runs on a background thread
    noise = np.random.randint(0, 256, (128, 128, 3), dtype=np.uint8)

    app.state["fps"] = min(app.target_fps,int(app.fps()))
    app.state["image"] = pype.PypeImage(noise).base64
    app.push(["image","fps"])
    pass

def nextPage(app):
    app.load_page(1)

def functionFromPython(app):
    app.log("I was called from the frontend side!")

def changed_count(app):
    count = app.state["count"]
    prevCount = app.previous_state["count"]

    if(count > prevCount):
        app.state["numbers"].append({"count":count, "color": f'rgb({random.randint(50,255)},{random.randint(50,255)},{random.randint(50,255)})'})
    elif(count < prevCount):
        app.state["numbers"].pop()

    app.log(f'Count changed to {count} from {prevCount}')    
    app.push(["numbers"])

app = pype.Pype("Testing",tools=False)

app.state["count"] = 0
app.state["numbers"] = []

app.push(["count","numbers"])

app.bind('count','count',HTMLAttributes.INNERHTML)
app.bind('fps','fps',HTMLAttributes.INNERHTML)
app.bind('image', 'image',HTMLAttributes.SRC)

app.hook('count',changed_count)
app.observe('numbers','prefab-number','number','prefab-parent')

app.expose(functionFromPython)
app.expose(nextPage)
app.run([generateImage],["index.html","new-page.html"])