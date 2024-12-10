from Pype import pype
import random
import numpy as np

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

app.bind('count','count',pype.HTMLAttributes.INNERHTML)

app.hook('count',changed_count)
app.observe('numbers','prefab-number','number','prefab-parent')

app.run([],["index.html"])