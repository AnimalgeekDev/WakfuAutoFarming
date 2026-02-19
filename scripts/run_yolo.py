from ultralytics import YOLO

def run_yolo_model(model_path, image_path):
    """
    Run a YOLO model on an image.

    Args:
        model_path (str): Path to the trained YOLO model file.
        image_path (str): Path to the image to run detection on.
    """
    # Load the trained YOLO model
    model = YOLO(model_path)

    # Perform detection
    results = model.predict(source=image_path, save=True, show=True)

    # Print results
    print("Detection results:", results)

if __name__ == "__main__":
    # Example usage
    trained_model_path = "runs/detect/train/weights/best.pt"  # Replace with the actual path to your trained model
    test_image_path = "train_data/test/images/Captura-de-pantalla-16-_png.rf.ab008854e0449d7133e0a1ef9158e3cf.jpg"  # Replace with the actual path to your test image
    run_yolo_model(model_path=trained_model_path, image_path=test_image_path)