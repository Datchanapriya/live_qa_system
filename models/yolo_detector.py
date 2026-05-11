from ultralytics import YOLO


class YOLODetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.6):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.history = []

    def detect_objects(self, frame):
        results = self.model(frame, verbose=False)
        object_counts = {}

        for r in results:
            for box in r.boxes:
                # Ignore very small detections
                x1, y1, x2, y2 = box.xyxy[0]
                area = (x2 - x1) * (y2 - y1)

                if area < 5000:
                    continue

                confidence = float(box.conf[0])
                if confidence < self.conf_threshold:
                    continue

                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]

                if class_name in object_counts:
                    object_counts[class_name] += 1
                else:
                    object_counts[class_name] = 1

        # ---- Temporal smoothing ----
        self.history.append(object_counts)

        if len(self.history) > 5:
            self.history.pop(0)

        smoothed = {}
        for frame_objects in self.history:
            for obj, count in frame_objects.items():
                smoothed[obj] = smoothed.get(obj, 0) + count

        for obj in smoothed:
            smoothed[obj] = round(smoothed[obj] / len(self.history))

        return smoothed
