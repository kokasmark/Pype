import sys
import os

# Get the parent directory (where pype.py is located)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


import pype
from pype import HTMLAttributes
import random

def updatingFunc(app):
    #this function runs on a background thread
    # count = app.get_state("count")
    # app.set_state("count",count+1)
    pass

def nextPage(app):
    app.load_page(1)

def functionFromPython(app):
    app.log("I was called from the frontend side!")

def changed_count(app):
    count = app.get_state("count")
    prevCount = app.get_prev_state("count")

    numbers = app.get_state("numbers")

    if(count > prevCount):
        random_color = f'rgb({random.randint(50,255)},{random.randint(50,255)},{random.randint(50,255)})'
        attr = {"count":count, "color": random_color}
        numbers.append(attr)
        app.set_state("numbers", numbers)
    elif(count < prevCount):
        numbers.pop()
        app.set_state("numbers", numbers)

    app.log(f'Count changed to {count} from {prevCount}')

app = pype.Pype("Testing",tools=False)

app.set_state("count",0)
app.set_state("numbers", [])
app.bind('count','count',HTMLAttributes.INNERHTML)
app.hook('count',changed_count)
app.observe('numbers','prefab-number','number','prefab-parent')

app.expose(functionFromPython)
app.expose(nextPage)
app.run([updatingFunc],["index.html","new-page.html"])