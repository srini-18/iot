from flask import Flask, request, jsonify, render_template
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)

# Load YOLO model once (important for performance)
model = YOLO("yolov8n.pt")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect():
    try:
        data = request.json.get("image")

        if not data:
            return jsonify({"error": "No image received"}), 400

        # Decode base64 image
        img_data = base64.b64decode(data.split(",")[1])
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Run YOLO inference
        results = model(frame)

        detections = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                detections.append({
                    "class": model.names[int(box.cls)],
                    "confidence": float(box.conf),
                    "box": {
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2
                    }
                })

        return jsonify({"detections": detections})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Use PORT env var provided by hosting platforms (e.g., Azure Web App)
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
