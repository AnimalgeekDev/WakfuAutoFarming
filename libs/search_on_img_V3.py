import cv2
import numpy as np

def search_template_on_img(template, img, tolerancy):
    # Convertir la imagen de la botella a escala de grises
    # Convertir la imagen de la botella a escala de grises
    gray_botella = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Crear el detector ORB
    orb = cv2.ORB_create()

    # Encontrar los puntos clave y los descriptores con ORB
    kp1, des1 = orb.detectAndCompute(gray_botella, None)
    kp2, des2 = orb.detectAndCompute(img, None)

    # Usar el método de fuerza bruta para encontrar todas las correspondencias
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Filtrar los emparejamientos basados en el umbral de distancia
    matches_filtrados = [match for match in matches if match.distance > tolerancy]

    if len(matches_filtrados) > 0:
        # Seleccionar el mejor emparejamiento después de filtrar
        best_match = min(matches_filtrados, key=lambda x: x.distance)

        # Obtener las coordenadas de los puntos clave en ambas imágenes
        pt1 = kp1[best_match.queryIdx].pt
        pt2 = kp2[best_match.trainIdx].pt
    
        # Seleccionar la mejor coincidencia
        best_match = matches_filtrados[0]

        # Obtener las coordenadas de los puntos clave en ambas imágenes
        pt1 = kp1[best_match.queryIdx].pt
        x, y = kp2[best_match.trainIdx].pt

        # Dibujar la mejor coincidencia en una imagen
        img_matches = cv2.drawMatches(template, kp1, img, kp2, [best_match], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        return (x, y, tolerancy, best_match.distance, img_matches)

    return (0,0, tolerancy, 0, img)