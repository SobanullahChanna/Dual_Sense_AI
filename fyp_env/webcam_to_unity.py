import cv2
import mediapipe as mp
import socket
import math
import numpy as np

# Network Setup (Matches your Unity C# script)
UDP_IP = "127.0.0.1" 
UDP_PORT = 5052
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# MediaPipe AI Setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open the Webcam
cap = cv2.VideoCapture(0)

print("🤖 Computer Vision Online! Step back so the camera can see your arm.")

# Helper function to calculate the angle between 3 points (Hip, Shoulder, Elbow)
def calculate_angle(a, b, c):
    a = np.array(a) # Hip
    b = np.array(b) # Shoulder
    c = np.array(c) # Elbow
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    # Recolor image to RGB for MediaPipe
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    
    # AI processing: Find the skeleton!
    results = pose.process(image)
    
    # Recolor back to BGR for OpenCV display
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # If the AI sees a human body...
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        try:
            # Get coordinates for Right Hip (24), Right Shoulder (12), and Right Elbow (14)
            hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            
            # Calculate the real-time angle of your arm
            arm_angle = calculate_angle(hip, shoulder, elbow)
            
            # Since Unity's Z-axis works a bit differently, we subtract from 180 to align the math
            unity_angle = 180 - arm_angle
            
            # Send the angle to Unity!
            data_string = f"{unity_angle:.2f}"
            sock.sendto(data_string.encode(), (UDP_IP, UDP_PORT))
            
            # Put the angle text on your screen so you can see it
            cv2.putText(image, f"Arm Angle: {int(unity_angle)}", 
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
        except Exception as e:
            pass
            
        # Draw the skeleton lines on the video
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
    # Show the video window
    cv2.imshow('FYP - MediaPipe Live Tracking', image)

    # Press 'q' to quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()