from ultralytics import YOLO

def main():
    """Run YOLO11 inference."""
    # Load model
    model = YOLO("yolo11m.pt")

    # Run inference
    results = model()


if __name__ == "__main__":
    main()
