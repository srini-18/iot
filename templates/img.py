import cv2
import numpy as np

# Create blank image
img = np.ones((400, 600, 3), dtype=np.uint8) * 255

# Draw Cat (detected)
cv2.rectangle(img, (50, 100), (150, 250), (0, 255, 0), 3)
cv2.putText(img, 'Cat', (55, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Draw Dog (detected)
cv2.rectangle(img, (250, 100), (400, 250), (0, 255, 0), 3)
cv2.putText(img, 'Dog', (255, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Draw Ball (missed detection, no box)
cv2.circle(img, (500, 180), 30, (128, 128, 128), -1)
cv2.putText(img, 'Ball', (485, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
cv2.putText(img, 'Missed!', (470, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# Save or display
cv2.imwrite('object_detection_missed_detection.png', img)
cv2.imshow('Missed Detection Example', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
