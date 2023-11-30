import cv2
import random

def search_template_on_img(template , img , tolerancy):
    # Convertir las imágenes a escala de grises
    template_mod  = template #cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    img_mod  = img #cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Inicializar el detector SIFT
    sift = cv2.SIFT_create()

    # Encontrar los puntos clave y los descriptores con SIFT
    keypoints_query, descriptors_query = sift.detectAndCompute(template_mod, None)
    keypoints_img, descriptors_img = sift.detectAndCompute(img_mod, None)

    # Utilizar el matcher de fuerza bruta para encontrar las coincidencias entre descriptores
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors_query, descriptors_img, k=2)

    # Aplicar la relación de prueba de razón para obtener buenas coincidencias
    good_matches = []
    for m, n in matches:
        if m.distance < tolerancy * n.distance:
            good_matches.append(m)

    if len(good_matches) > 0:
        # Obtener la mejor coincidencia
        best_match = max(good_matches, key=lambda x: x.distance)

        # Obtener las coordenadas (x, y) de la mejor coincidencia en la imagen de la captura de pantalla
        x, y = keypoints_img[best_match.trainIdx].pt

        img_match = cv2.drawMatches(template_mod, keypoints_query, img_mod, keypoints_img, [best_match], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        return (int(x + random.randrange(20)), int(y + random.randrange(20)), tolerancy * n.distance, m.distance, img_match)

    return (0, 0, tolerancy * n.distance, m.distance, None)