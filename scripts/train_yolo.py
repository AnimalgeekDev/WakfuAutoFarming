"""Simple training script for YOLO models.

This script is intended to be executed independently of the GUI.
It reads configuration from `scripts/.env` and iterates over the provided
epochs array, running `model.train` for each epoch value and setting the
run `name` to include the model name and epoch count.

Environment variables expected in `scripts/.env`:
    DATA_PATH: path to dataset yaml
    MODEL_NAME: model name or weights path (e.g. yolov8n or path/to/weights.pt)
    EPOCHS: comma separated epoch values (e.g. 25,50,75)
    DEVICE: device string for ultralytics (e.g. 'cpu' or '0')
    PROJECT_NAME: project folder for results
    IMGZ: image size (optional)

Usage: run `python scripts/train_yolo.py` after filling `scripts/.env`.
"""

import os
from typing import List
from ultralytics import YOLO
from dotenv import load_dotenv


def _parse_epochs(value: str) -> List[int]:
    parts = [p.strip() for p in value.split(",") if p.strip()]
    return [int(p) for p in parts]


def main() -> None:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
    data_path = os.getenv("DATA_PATH")
    model_name = os.getenv("MODEL_NAME")
    epochs_raw = os.getenv("EPOCHS")
    device = os.getenv("DEVICE")
    project = os.getenv("PROJECT_NAME")
    imgsz = os.getenv("IMGZ")
    batch = os.getenv("BATCH_SIZE")

    epochs = _parse_epochs(epochs_raw)

    for e in epochs:
        name = f"{os.path.basename(model_name)}-{e}_epochs"
        model = YOLO(model_name)
        kwargs = {"data": data_path, "epochs": e, "project": project, "name": name, "device": device, "imgsz": int(imgsz), "batch": int(batch)}

        print(f"Starting training: model={model_name} epochs={e} project={project} name={name} device={device} imgsz={imgsz} batch={batch}")
        model.train(**kwargs)


if __name__ == "__main__":
    main()
