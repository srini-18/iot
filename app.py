from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
import random
from collections import defaultdict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
frame_wid = 640
frame_height = 480

# Load class list from file
def load_class_list(file_path):
    try:
        with open(file_path, "r") as f:
            class_list = f.read().splitlines()
        return class_list
    except FileNotFoundError:
        print(f"Error: Class list file '{file_path}' not found.")
        return
    except Exception as e:
        print(f"Error loading class list: {e}")
        return

# Generate random color codes for object detection
def color_code(class_list):
    detection_colors = {}
    for class_name in class_list:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        detection_colors[class_name] = (b, g, r)
    return detection_colors

# Load YOLO model
def load_model():
    try:
        model = YOLO("yolov8n.pt")  # Ensure YOLOv8 model is available
        return model
    except Exception as e:
        print(f"Error loading YOLO model: {e}")
        return None

# Object detection function
def object_detection(class_list, detection_colors, model, 
                     frame):
    detected_objects = defaultdict(dict)
    try:
        results = model.predict(frame)
        for result in results:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                if  confidence > 0.5:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    class_name = class_list[class_id]
                    color = detection_colors.get(class_name, (0, 0, 0))  # Get color or default to black
                    detected_objects[class_name] = {
                        'confidence': confidence,
                        'box': [x1, y1, x2, y2],
                        'color': color
                    }
        return detected_objects
    except Exception as e:
        print(f"Error during object detection: {e}")
        return defaultdict(dict)

# Flask Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/coco')
def coco():
    return render_template('coco.html')

@app.route('/main')
def main():
    return render_template('main.html')  # Main content - 4th page

@app.route('/applications')
def applications():
    return render_template('applications.html')


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/detect', methods=['POST'])
def detect_objects_route():
    try:
        # Receive frame from frontend
        file = request.files['frame'].read()
        npimg = np.frombuffer(file, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if frame is None:
            raise ValueError("Could not decode the image.")

        # Object detection
        objects = object_detection(class_list, detection_color, model, frame)

        # Convert defaultdict to a regular dict before jsonify
        objects_dict = {}
        for key, value in objects.items():
            objects_dict[key] = value

        return jsonify(objects_dict)  # Return the dictionary

    except (KeyError, ValueError, cv2.error, Exception) as e:
        print(f"Error during detection: {e}")
        return jsonify({"error": str(e)}), 500  # HTTP 500 for server error

if __name__ == '__main__':
    class_list = load_class_list("coco_class.txt")
    if not class_list:
        print("Error: Could not load class list. Exiting.")
        exit()

    detection_color = color_code(class_list)
    model = load_model()
    if model is None:
        print("Error: Could not load YOLO model. Exiting.")
        exit()

    app.run(debug=True)