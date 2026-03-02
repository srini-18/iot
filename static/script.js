const video = document.getElementById("webcam-feed") || document.getElementById("video");
const startButton = document.getElementById("start-detection");
const detectionResultsDiv = document.getElementById("detection-results");

let detectionTimer = null;

async function startWebcam() {
    if (!video || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        return;
    }
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        await video.play();
    } catch (error) {
        console.error("Webcam access failed:", error);
        if (detectionResultsDiv) {
            detectionResultsDiv.textContent = "Unable to access webcam.";
        }
    }
}

function renderDetections(detections) {
    if (!detectionResultsDiv) {
        return;
    }
    if (!detections || detections.length === 0) {
        detectionResultsDiv.textContent = "No objects detected.";
        return;
    }
    const items = detections
        .slice(0, 8)
        .map((d) => `${d.class} (${(d.confidence * 100).toFixed(1)}%)`);
    detectionResultsDiv.textContent = `Detected: ${items.join(", ")}`;
}

async function captureAndDetect() {
    if (!video || video.readyState < 2) {
        return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imageData = canvas.toDataURL("image/jpeg");

    try {
        const response = await fetch("/detect", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: imageData })
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || "Detection failed");
        }
        renderDetections(result.detections);
    } catch (error) {
        console.error("Detection error:", error);
        if (detectionResultsDiv) {
            detectionResultsDiv.textContent = "Detection failed.";
        }
    }
}

function toggleDetection() {
    if (!startButton) {
        return;
    }
    if (detectionTimer) {
        clearInterval(detectionTimer);
        detectionTimer = null;
        startButton.textContent = "Start Detection";
        return;
    }

    captureAndDetect();
    detectionTimer = setInterval(captureAndDetect, 1500);
    startButton.textContent = "Stop Detection";
}

startWebcam();
if (startButton) {
    startButton.addEventListener("click", toggleDetection);
}
