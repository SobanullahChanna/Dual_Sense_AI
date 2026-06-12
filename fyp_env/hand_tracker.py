import cv2
import mediapipe as mp

# 1. Initialize the MediaPipe Hands AI
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils # This is the "paintbrush" to draw the skeleton

# 2. Turn on the webcam (Camera 0)
cap = cv2.VideoCapture(0)
print("Opening AI Tracker... Press 'q' on your keyboard to close!")

# 3. Set up the tracking model (50% confidence threshold to avoid false positives)
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        # 4. Color Conversion (CRITICAL)
        # OpenCV reads video in BGR (Blue, Green, Red) format.
        # MediaPipe AI only understands RGB (Red, Green, Blue) format. 
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 5. The Brains: Process the frame to find hands
        results = hands.process(image)

        # 6. Convert the color back so OpenCV can display it normally
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 7. Draw the Skeleton
        # If the AI found hands, draw the dots and connecting lines
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS
                )

        # 8. Show the final image on screen
        cv2.imshow('Dual-Sense AI: Hand Tracking', image)

        # 9. Wait for the 'q' key to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Clean up
cap.release()
cv2.destroyAllWindows()