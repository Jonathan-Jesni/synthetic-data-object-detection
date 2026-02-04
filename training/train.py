from ultralytics import YOLO

model = YOLO("runs/detect/train2/weights/best.pt")

model.train(
    data="dataset/data.yaml",
    epochs=100,
    imgsz=640,
    batch=8,
    device="cpu",
    name="train3"
)
