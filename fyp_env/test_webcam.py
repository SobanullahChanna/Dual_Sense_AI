import cv2

print("Opening webcam... Press the 'q' key on your keyboard to close the window!")

# The '0' tells Python to use your computer's default webcam
cap = cv2.VideoCapture(0)

while True:
    # Read the video frame by frame
    success, frame = cap.read()
    
    if not success:
        print("Error: Could not read from webcam.")
        break

    # Show the video feed in a popup window
    cv2.imshow("Dual-Sense AI: Eyes Test", frame)

    # Wait 1 millisecond for the 'q' key to be pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up and turn off the camera
cap.release()
cv2.destroyAllWindows()