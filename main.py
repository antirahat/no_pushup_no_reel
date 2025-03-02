import cv2

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# Initialize video capture from default camera (usually 0)
cap = cv2.VideoCapture(0)

while True:
    # Read frame from the camera
    ret, img = cap.read()
    
    # Break the loop if frame is not read correctly
    if not ret:
        break
        
    # Your image processing code will go here
    
    # Display the frame
    cv2.imshow('Video', img)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()