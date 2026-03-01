import os
from typing import List
from ultralytics import YOLO
from dotenv import load_dotenv


def _parse_epochs(value: str) -> List[int]:
    parts = [p.strip() for p in value.split(",") if p.strip()]
    return [int(p) for p in parts]


def main() -> None:
    load_dotenv()
    
    model_name = os.getenv("MODEL_NAME")
    data_path = os.getenv("DATA_PATH")
    device = os.getenv("DEVICE")
    project = os.getenv("PROJECT_NAME")
    imgsz = os.getenv("IMGZ")
    batch = os.getenv("BATCH_SIZE")
    
    epochs_raw = os.getenv("EPOCHS")
    epochs = _parse_epochs(epochs_raw)

    for epoch in epochs:
        name = f"{os.path.basename(model_name)}-{epoch}_epochs"
        model = YOLO(model_name)
        kwargs = {
            "data": data_path, 
            "epochs": epoch,
            "project": project, 
            "name": name,
            "device": device,
            "imgsz": int(imgsz),
            "batch": int(batch)
        }

        print(f"Starting training: model={model_name} epochs={epoch} project={project} name={name} device={device} imgsz={imgsz} batch={batch}")
        model.train(**kwargs)


if __name__ == "__main__":
    main()
