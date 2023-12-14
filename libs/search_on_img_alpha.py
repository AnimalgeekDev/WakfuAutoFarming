import cv2
import random

# Create sift
sift = cv2.SIFT_create()

# Create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

def search_template_on_img(img, template, tolerancy):
    # Leer las imágenes
    img_grande = img
    img_pequena = template

    # Extraer el canal alpha de la imagen pequeña
    alpha_pequena = img_pequena[:, :, 3]

    # Encontrar las coordenadas de la región donde se encuentra la imagen pequeña en la imagen grande
    coincidencias = cv2.matchTemplate(img_grande[:, :, :3], img_pequena[:, :, :3], cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(coincidencias)
    
    better = cv2.rectangle(img_grande.copy(), max_loc, (max_loc[0] + img_pequena.shape[1], max_loc[1] + img_pequena.shape[0]), (0, 255, 0), 2)

    if max_val > tolerancy:
        middle_w = img_pequena.shape[1]
        middle_h = img_pequena.shape[0]

        pos_x = max_loc[0] + (middle_w // 2) + random.randint(-(middle_w // 35), middle_w // 35)
        pos_y = max_loc[1] + (middle_h // 2) + random.randint(-(middle_h // 35), middle_h // 35)

        return (pos_x, pos_y, tolerancy, max_val, better)    
    
    return (0, 0, tolerancy, max_val, better)