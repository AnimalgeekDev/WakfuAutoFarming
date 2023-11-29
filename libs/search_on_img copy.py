import cv2
import numpy as np

def search_template_on_img(botella_transparente , captura_pantalla , tolerancy):
    # Leer las imágenes de la botella y la captura de pantalla
    query_image = botella_transparente
    screenshot = captura_pantalla

    # Convertir las imágenes a escala de grises
    query_gray = cv2.cvtColor(query_image, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Inicializar el detector SIFT
    sift = cv2.SIFT_create()

    # Encontrar los puntos clave y los descriptores con SIFT
    keypoints_query, descriptors_query = sift.detectAndCompute(query_gray, None)
    keypoints_screenshot, descriptors_screenshot = sift.detectAndCompute(screenshot_gray, None)

    # Utilizar el matcher de fuerza bruta para encontrar las coincidencias entre descriptores
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors_query, descriptors_screenshot, k=2)

    # Aplicar la relación de prueba de razón para obtener buenas coincidencias
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Dibujar las coincidencias en una imagen
    img_matches = cv2.drawMatches(query_image, keypoints_query, screenshot, keypoints_screenshot, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # Mostrar la imagen de coincidencias
    cv2.imshow("Matches", img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # result = cv2.matchTemplate(img.astype(np.uint8), template.astype(np.uint8), cv2.TM_CCOEFF_NORMED)

    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # print("Highest correlation: ", max_val)
    # print("Lowest correlation: ", min_val)

    # x, y = max_loc
    # h, w, _ = template.shape

    # posX = 0 if max_val < tolerancy else x+(w//2)
    # posY = 0 if max_val < tolerancy else y+(h//2)
    
    return (0,0)