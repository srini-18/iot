const video = document.getElementById('webcam-feed');
const startDetectionButton = document.getElementById('start-detection');
const detectionResultsDiv = document.getElementById('detection-results');

// Get user's webcam
navigator.mediaDevices.getUserMedia({
        video: true
    })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => console.error("Error accessing webcam:", err));
startDetectionButton.addEventListener('click', () => {
    captureAndDetect();
});
function captureAndDetect() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('frame', blob, 'frame.jpg');
        fetch('http://localhost:5000/detect', { // Adjust if your backend is on a different port
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Detection error:", data.error);
                detectionResultsDiv.textContent = "Error during detection.";
            } else {
                displayDetectionResults(data);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            detectionResultsDiv.textContent = "Error connecting to detection server.";
        });
    }, 'image/jpeg');
}

function displayDetectionResults(results) {
    let resultsText = "Detected Objects: ";
    for (const item in results) {
        resultsText += `${item} (${results[item].confidence.toFixed(2)}) `;
    }
    detectionResultsDiv.textContent = resultsText;
}