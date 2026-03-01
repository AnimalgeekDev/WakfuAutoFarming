import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import glob
import os
from typing import List, Dict, Tuple


class TemplateMatcher:
    def __init__(self, templates_path: str):
        self.templates_path = templates_path
        self.templates = []
        self.template_names = []
        self.load_templates()

    def load_templates(self) -> List[str]:
        self.templates = []
        self.template_names = []

        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff']

        for ext in image_extensions:
            for template_path in glob.glob(os.path.join(self.templates_path, ext)):
                template = cv2.imread(template_path, cv2.IMREAD_COLOR)

                if template is not None:
                    self.templates.append(template)
                    self.template_names.append(Path(template_path).stem)

        return self.template_names

    def template_match(
        self,
        image: Image.Image,
        method: int,
        threshold: float,
        max_overlap: float
    ) -> List[Dict]:

        if not isinstance(image, Image.Image):
            raise ValueError("Tipo de imagen no soportado")

        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        detections = []

        for template, template_name in zip(self.templates, self.template_names):

            h, w, _ = template.shape

            result_match = cv2.matchTemplate(img, template, method)

            # if method not in [cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED]:
            #     cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX)

            # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            #     result = 1 - result

            ys, xs = np.where(result_match >= threshold)

            rects_match = []
            confidences = []

            for (x, y) in zip(xs, ys):
                rects_match.append([int(x), int(y), int(w), int(h)])
                confidences.append(float(result_match[y, x]))

            if len(rects_match) > 0 and len(rects_match) < 500:
                group_threshold = 1
                
                double_math = rects_match + rects_match

                rects, confidences = cv2.groupRectangles(
                    double_math,
                    group_threshold,
                    max_overlap
                )

                for (box, confidence) in zip(rects, confidences):
                    x, y, w, h = box

                    detections.append({
                        "box": [int(x), int(y), int(x + w), int(y + h)],
                        "confidence": float(confidence),
                        "class": template_name
                    })

        return sorted(detections, key=lambda x: x["confidence"], reverse=True)