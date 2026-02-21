from ultralytics import YOLO


def train_yolo_model(data_path, model_type, epochs, project='wakfu', name='train_logs'):
    """
    Train a YOLO model.

    Args:
        data_path (str): Path to the dataset YAML file.
        model_type (str): Type of YOLO model to use (e.g., 'yolov8n', 'yolov8s').
        epochs (int): Number of training epochs.
        project (str): Directory to save training results and logs.
        name (str): Name of the training run.
    """
    # Initialize the YOLO model
    model = YOLO(model_type)

    # Train the model with TensorBoard logging enabled
    model.train(data=data_path, epochs=epochs, project=project, name=name)


if __name__ == "__main__":
    # Define training configurations
    training_configs = [
        # {"dataset_path": "train_data/WakfuFarming.v3i.yolov8/data.yaml", "models": [
        #     {"model_name": "yolov8n", "epochs": [10, 25, 50, 75]},
        #     {"model_name": "yolov8s", "epochs": [10, 25, 50, 75]}
        # ]},
        {"dataset_path": "train_data/WakfuFarming.v3i.yolo26/data.yaml", "models": [
            {"model_name": "yolo26n", "epochs": [10, 25, 50, 75]},
            {"model_name": "yolo26s", "epochs": [10, 25, 50, 75]}
        ]}
    ]

    # Train models based on configurations
    for config in training_configs:
        dataset_path = config["dataset_path"]
        for model_config in config["models"]:
            model_name = model_config["model_name"]
            for epoch in model_config["epochs"]:
                folder_name = f"{model_name}-{epoch}"
                train_yolo_model(
                    data_path=dataset_path, model_type=model_name, epochs=epoch, name=folder_name)
