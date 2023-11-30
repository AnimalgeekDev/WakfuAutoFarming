import numpy as np
import cv2
import mss 

from libs import search_on_img
from libs import load_files
from libs import debuger
from libs import clicks
from libs import delay

# Parameters
debug = True
farming_icons = "farming_icons"
farming_actions = "farming_actions"
reducer_scaling = 4
mon_number = 0
tolerancy = 0.5
num_intents = 10

# Globals
templateUrlsIcons = []
templatesIcons = []
templateUrlsActions = []
templatesActions = []

sct = None
mon = None
w = 0
h = 0

intents = 0

# Estado:
state = 0

# 0: Buscar recursos
# 1: Ubicando mouse and click
# 2: Buscando acciones posibles
# 3: Ubicando mouse and click en accion

# Load files templates using cv2
def load_template_data():
    global templatesIcons, templateUrlsIcons
    debuger.write("Read files to template", debug)
    templateUrlsIcons = load_files.get_templates(farming_icons)

    debuger.write(f"Files to template {templateUrlsIcons}", debug)
    
    debuger.write("Read files using opencv to template", debug)
    templatesIcons = load_files.import_templates(templateUrlsIcons)

def load_action_data():
    global templatesActions, templateUrlsActions
    debuger.write("Read files to actions", debug)
    templateUrlsActions = load_files.get_templates(farming_actions)

    debuger.write(f"Files to actions {templateUrlsActions}", debug)
    
    debuger.write("Read files using opencv to actions", debug)
    templatesActions = load_files.import_templates(templateUrlsActions)

def set_monitor():
    global sct, mon, w, h

    sct = mss.mss()

    mon = sct.monitors[1:][mon_number]
    w = mon['width']
    h = mon['height']

def get_screenshot():
    img = np.array(sct.grab(mon))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

def valid_pos_item(img):
    for index, template in enumerate(templatesIcons):
        x, y, tol, dec, match = search_on_img.search_template_on_img(template, img, tolerancy)
        imgName = templateUrlsIcons[index].split("\\")[-1]

        if x > 0 and y > 0:
            debuger.write(f'Pos item detect {imgName}: ({x},{y}); (dec < tol): ({tol},{dec})', debug)

            if debug:
                debuger.print_mini(reducer_scaling, imgName, match, x, y, w, h)
            return (x , y)
    
    return (0,0)

def valid_pos_action(img):
    for index, template in enumerate(templatesActions):
        x, y, tol, dec, match = search_on_img.search_template_on_img(template, img, tolerancy)
        imgName = templateUrlsActions[index].split('\\')[-1]

        if x > 0 and y > 0:
            debuger.write(f'Pos action detect {imgName}: ({x},{y}); (dec < tol): ({dec},{tol})', debug)
            
            if debug:
                debuger.print_mini(reducer_scaling, imgName, match, x, y, w, h)
            return (x , y)
    return (0,0)

def run_farming():
    global state, intents

    # Pos detection
    x = 0
    y = 0

    debuger.write('Search item', debug)
    while True:
        if state == 0:
            screen = get_screenshot()
            x, y = valid_pos_item(screen)

            if x > 0 and y > 0:
                state = 1 #item detect

        if state == 1:
            debuger.write('Right click item', debug)
            clicks.right_click(x, y)
            state = 2 #click ok and go to search actions
            debuger.write('Search Actions', debug)

        if state == 2:
            screen = get_screenshot()
            x, y = valid_pos_action(screen)
            
            if x > 0 and y > 0:
                state = 3 #action detect
                debuger.write('Action Detected', debug)
            else:
                intents += 1
                if intents >= num_intents:
                    state = 0
                    debuger.write('Reset, go to search item', debug)
        
        if state == 3:
            debuger.write('Click actions', debug)
            clicks.right_click(x, y)
            state = 0 #reset process
            delay.wait(4)
            debuger.write('Search item', debug)

        if cv2.waitKey(1) == ord('q'):
            debuger.write('Close', debug)
            cv2.destroyAllWindows()
            break

        if cv2.waitKey(1) == ord('r'):
            state = 0
            debuger.write('Reset', debug)

# Load data
load_template_data()
load_action_data()
set_monitor()

# Run farming script
run_farming()