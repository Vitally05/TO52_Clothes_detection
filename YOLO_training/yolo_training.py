import torch
from ultralytics import YOLO

if __name__ == '__main__':
    import multiprocessing

    multiprocessing.freeze_support()

    # Load your model here
    model = YOLO('../yolov8n.pt')  # Adjust the model name based on your specific setup

    # Train the model
    results = model.train(data='config.yaml', epochs=32, device='cuda')
