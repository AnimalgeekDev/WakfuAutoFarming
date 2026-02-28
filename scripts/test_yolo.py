import os
import cv2 as cv
from ultralytics import YOLO
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
    model_path = os.getenv("MODEL_PATH")
    test_path = os.getenv("TEST_PATH")
    imgsz = os.getenv("IMGZ")
    
    test_files = [os.path.join(test_path, f) for f in os.listdir(test_path) if os.path.isfile(os.path.join(test_path, f))]
    model = YOLO(model_path)
    
    print(f"Testing model {model_path} on {len(test_files)} images from {test_path} with img size {imgsz}...")
    
    # for file in test_files:
    #     print(f"Testing on {file}...")
    model.predict(source=test_files, save=True, show=True, imgsz=int(imgsz))