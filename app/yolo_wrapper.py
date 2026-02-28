"""Wrapper around Ultralytics YOLO model for clean usage in the app.

This module provides `YoloModel` which loads a model and exposes a `predict`
method that returns a simplified list of detections filtered by confidence.
"""
from typing import List, Dict
from PIL import Image
import numpy as np


class YoloModel:
    """Simple wrapper around an Ultralytics YOLO model instance.

    Methods:
        load: load the model from a given path
        predict: run inference on a PIL image and return detections
    """

    def __init__(self) -> None:
        self.model = None

    def load(self, model_path: str, device: str, img_size: int) -> None:
        """Load the YOLO model from `model_path`.

        Args:
            model_path: relative path to the model weights.
            device: device string for ultralytics (e.g. 'cpu' or '0').
            img_size: image size to pass to predict (imgsz).

        Raises:
            Exception: if model loading fails.
        """
        try:
            from ultralytics import YOLO

            self.model = YOLO(model_path)
            # store config
            self.device = device
            self.img_size = img_size
        except Exception as exc:
            raise Exception(f"YoloModel.load: failed to load model: {exc}")

    def predict(self, image: Image.Image, conf_threshold: float) -> List[Dict]:
        """Run prediction on a PIL image and return filtered detections.

        Returned detection dict format:
            {'label': str, 'confidence': float, 'xyxy': (x1,y1,x2,y2)}

        Args:
            image: PIL image to process.
            conf_threshold: minimum confidence to keep detection.

        Returns:
            List[Dict]: list of detections.

        Raises:
            Exception: if prediction fails or model not loaded.
        """
        if self.model is None:
            raise Exception("YoloModel.predict: model is not loaded")

        try:
            results = self.model.predict(source=image, imgsz=self.img_size, save=True)
            detections = []
            for r in results:
                boxes = getattr(r, "boxes", None)
                if boxes is None:
                    continue
                for box in boxes:
                    conf = float(box.conf.cpu().numpy()) if hasattr(box, "conf") else float(box.conf)
                    if conf < conf_threshold:
                        continue
                    xyxy = tuple(map(float, box.xyxy.cpu().numpy()[0])) if hasattr(box, "xyxy") else tuple(map(float, box.xyxy))
                    cls = int(box.cls.cpu().numpy()[0]) if hasattr(box, "cls") else int(box.cls)
                    label = self.model.names[cls] if hasattr(self.model, "names") else str(cls)
                    detections.append({"label": label, "confidence": conf, "xyxy": xyxy})
            return detections
        except Exception as exc:
            raise Exception(f"YoloModel.predict: prediction failed: {exc}")
