import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO('../yolov8n.pt')

# Threshold for red color detection
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Load video
video_path = "../volei2.mp4"
cap = cv2.VideoCapture(video_path)

ret = True
# Read frames
while ret:
    ret, frame = cap.read()

    if ret:
        # Convert frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create a mask for red color
        mask = cv2.inRange(hsv_frame, lower_red, upper_red)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate through contours
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:  # Adjust this threshold as needed
                # Draw rectangle around detected object
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break 

cap.release()
cv2.destroyAllWindows()
