import sys
import os

# Get the parent directory (where pype.py is located)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)


import pype

prev_count = 0
def updatingFunc(app):
    global prev_count

    count = app.get_state("count")

    if prev_count != count:
        print('\33[102m' + ' Pype ' + '\33[0m'+f" New count value: {app.get_state('count')}")
        prev_count = count

app = pype.Pype("Testing",build="prod")
app.set_state("count",prev_count)
app.bind('count','count')
app.run([updatingFunc])