import cv2
import numpy as np
from win32api import keybd_event
from time import sleep

# Virtual key code for down arrow
VK_DOWN = 0x28

# Load the pre-trained face detection model
face_net = cv2.dnn.readNet(
    r"c:\Users\rahat\OneDrive\Desktop\Learning materials\no_pushup_no_reel\deploy.prototxt.txt",
    r"c:\Users\rahat\OneDrive\Desktop\Learning materials\no_pushup_no_reel\res10_300x300_ssd_iter_140000.caffemodel"
)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize variables for head tracking
prev_y = None
movement_threshold = 30  # Adjust this value based on sensitivity needs
cooldown = 0  # Cooldown counter for key press

while True:
    # Read frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Get frame dimensions
    h, w = frame.shape[:2]

    # Create a blob from the frame
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], False, False)
    
    # Set the blob as input and get detections
    face_net.setInput(blob)
    detections = face_net.forward()

    # Process detections
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > 0.5:  # Confidence threshold
            # Get face coordinates
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            # Calculate center of the face
            current_y = (startY + endY) // 2
            
            # Draw face rectangle
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            
            # Track vertical movement
            if prev_y is not None and cooldown == 0:
                movement = current_y - prev_y
                
                # If downward movement exceeds threshold
                if movement > movement_threshold:
                    # Simulate down arrow key press
                    keybd_event(VK_DOWN, 0, 0, 0)  # Key down
                    sleep(0.1)
                    keybd_event(VK_DOWN, 0, 2, 0)  # Key up
                    cooldown = 10  # Set cooldown to prevent rapid keypresses
            
            prev_y = current_y
            break  # Process only the first face detected
    
    # Update cooldown
    if cooldown > 0:
        cooldown -= 1

    # Display the frame
    cv2.imshow('Head Tracking', frame)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()