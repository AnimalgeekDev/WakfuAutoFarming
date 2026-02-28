"""Image processing helpers: centers calculation and overlays.

All functions here are small, well-typed, and documented for clarity.
"""
from typing import List, Tuple, Dict
from PIL import Image, ImageDraw
import random

def transform_yolo_coordinates_to_original(detections, width_org, height_org, scal_x, scal_y, yolo_size):
    """
    Transforma las coordenadas de las predicciones del espacio 640x640
    al espacio de la imagen original
    
    Args:
        resultados: resultados de yolo.predict()
        w_original, h_original: dimensiones originales
        escala_x, escala_y: factores de escala aplicados
        target_size: tamaño objetivo (640)
    
    Returns:
        Lista de bounding boxes en coordenadas originales
    """
    
    detections_transformed = []
    
    for detection in detections:
        # Obtener coordenadas en el espacio de 640x640 (x1, y1, x2, y2)
        x1, y1, x2, y2 = detection["xyxy"]
        
        # Validar que las coordenadas estén dentro del rango esperado
        x1 = max(0, min(yolo_size, x1))
        y1 = max(0, min(yolo_size, y1))
        x2 = max(0, min(yolo_size, x2))
        y2 = max(0, min(yolo_size, y2))
        
        # Transformar a coordenadas originales (invertir la escala)
        x1_org = x1 * scal_x
        y1_org = y1 * scal_y
        x2_org = x2 * scal_x
        y2_org = y2 * scal_y
        
        # Validar límites de la imagen original
        x1_org = max(0, min(width_org, x1_org))
        y1_org = max(0, min(height_org, y1_org))
        x2_org = max(0, min(width_org, x2_org))
        y2_org = max(0, min(height_org, y2_org))
        
        detections_transformed.append({
            'box': [x1_org, y1_org, x2_org, y2_org],
            'box_yolo': [x1, y1, x2, y2],
            'confidence': float(detection["confidence"]),
            'label': detection["label"]
        })
    
    return detections_transformed


def compute_centers(detections: List[Dict]) -> List[Tuple[int, int]]:
    """Compute integer centers for a list of detections.

    Args:
        detections: list of dicts with key `box` (x1,y1,x2,y2).

    Returns:
        list of (x_center, y_center) tuples.
    """
    centers: List[Tuple[int, int]] = []
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        centers.append((cx, cy))
    return centers


def overlay_boxes(image: Image.Image, detections: List[Dict]) -> Image.Image:
    """Draw bounding boxes and labels on a copy of the image.

    Args:
        image: original PIL image.
        detections: list of detections with `xyxy`, `label`, `confidence`.

    Returns:
        PIL.Image.Image: annotated image.
    """
    img = image.copy()
    draw = ImageDraw.Draw(img)
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
        label = f"{det['label']} {det['confidence']:.2f}"
        draw.text((x1 + 4, y1 + 4), label, fill="red")
    return img


def overlay_centers(image: Image.Image, centers: List[Tuple[int, int]]) -> Image.Image:
    """Overlay colored points at provided centers on a copy of the image.

    Args:
        image: original PIL image.
        centers: list of (x,y) coordinates.

    Returns:
        PIL.Image.Image: annotated image.
    """
    img = image.copy()
    draw = ImageDraw.Draw(img)
    for cx, cy in centers:
        color = tuple(random.randint(0, 255) for _ in range(3))
        r = 4
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=color)
    return img


def find_nearest_index(centers: List[Tuple[int, int]], reference: Tuple[int, int]) -> int:
    """Return the index of the center closest to the reference point.

    Args:
        centers: list of (x,y) tuples.
        reference: (x,y) reference point.

    Returns:
        int: index of nearest center, or -1 if centers is empty.
    """
    if not centers:
        return -1
    rx, ry = reference
    best_idx = -1
    best_dist_sq = None
    for i, (cx, cy) in enumerate(centers):
        dx = cx - rx
        dy = cy - ry
        d2 = dx * dx + dy * dy
        if best_dist_sq is None or d2 < best_dist_sq:
            best_dist_sq = d2
            best_idx = i
    return best_idx
