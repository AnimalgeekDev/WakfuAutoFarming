import cv2
import numpy as np

def search_template_on_img(template, img, tolerancy):
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    x, y = max_loc
    h, w, _ = template.shape

    posX = 0 if max_val < tolerancy else x+(w//2)
    posY = 0 if max_val < tolerancy else y+(h//2)
    
    return (posX, posY, tolerancy, max_val, img)