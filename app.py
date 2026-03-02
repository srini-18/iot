from flask import Flask, request, jsonify, render_template
from ultralytics import YOLO
from ultralytics.nn.tasks import DetectionModel
import cv2
import numpy as np
import base64
import os
import torch

app = Flask(__name__)

# PyTorch 2.6+ defaults `torch.load(..., weights_only=True)`.
# Allowlist Ultralytics model class so YOLO weights load successfully.
try:
    torch.serialization.add_safe_globals([DetectionModel])
except Exception:
    pass

# Load YOLO model once (important for performance)
model = YOLO("yolov8n.pt")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/coco")
@app.route("/coco_examples")
def coco():
    return render_template("coco.html")


@app.route("/working")
def working():
    return render_template("working.html")


@app.route("/applications")
def applications():
    return render_template("applications.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/team")
def team():
    # Keep legacy link from templates working without 404.
    return render_template("applications.html")


@app.route("/detect", methods=["POST"])
def detect():
    try:
        payload = request.get_json(silent=True) or {}
        data = payload.get("image")

        if not data:
            return jsonify({"error": "No image received"}), 400

        # Decode base64 image
        if "," in data:
            data = data.split(",", 1)[1]
        img_data = base64.b64decode(data)
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({"error": "Invalid image data"}), 400

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
