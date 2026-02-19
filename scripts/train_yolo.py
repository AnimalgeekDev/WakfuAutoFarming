from ultralytics import YOLO

def train_yolo_model(data_path, model_type='yolov8n', epochs=10):
    """
    Train a YOLO model.

    Args:
        data_path (str): Path to the dataset YAML file.
        model_type (str): Type of YOLO model to use (e.g., 'yolov8n', 'yolov8s').
        epochs (int): Number of training epochs.
    """
    # Initialize the YOLO model
    model = YOLO(model_type)

    # Train the model
    model.train(data=data_path, epochs=epochs)

if __name__ == "__main__":
    # Example usage
    dataset_path = "train_data/data.yaml"  # Replace with the actual path to your dataset YAML file
    train_yolo_model(data_path=dataset_path, model_type='yolov8n', epochs=100)