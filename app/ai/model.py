from ultralytics import YOLO

# Load model once when application starts
model = YOLO("app/ai/best.pt")


def detect_food(image_path):
    results = model(image_path)

    foods = []

    for result in results:
        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            food_name = model.names[class_id]

            foods.append({
                "food": food_name,
                "confidence": round(confidence, 2)
            })

    return foods