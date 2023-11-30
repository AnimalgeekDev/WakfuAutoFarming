import cv2

def write(text, debug):
    if debug:
        print(text)
    return

def print_mini(reducer_scaling, name, img, x, y, w, h):
    initRecX = 0 if x - 20 < 0 else x - 20
    initRecY = 0 if y - 20 < 0 else y - 20
    endRecX = w - 10 if x + 40 > w else x + 40
    endRecY = h - 10 if y + 40 > h else y + 40

    # if x > 0 and y > 0:
        # cv2.rectangle(img, (initRecX, initRecY), (endRecX, endRecY), (0,0,200), 3)
        # cv2.putText(img, name, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,200), 3)
    
    cv2.imshow('screen', cv2.resize(img, (img.shape[1]//reducer_scaling, img.shape[0]//reducer_scaling)))