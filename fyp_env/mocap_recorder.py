import cv2
import mediapipe as mp
import json
import os

# Set up the MediaPipe AI for Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
# We only track 1 hand to keep the math clean and fast
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

# Create a master folder to save our mathematical dictionary
output_folder = "ASL_Dictionary"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

cap = cv2.VideoCapture(0)

print("🤖 Mocap Dictionary Recorder Online!")
print("Press 's' on your keyboard to SAVE the current hand pose.")
print("Press 'q' on your keyboard to QUIT.")

# Ask the terminal what word/letter we are recording first
current_word = input("\nWhich letter/word are you about to record? (e.g., a, b, yes): ").lower()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip the image like a mirror so it's easier for you to use
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    
    # Process the AI!
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    landmark_data = []

    # If the AI sees a hand, draw the skeleton and extract the math
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract the exact 3D coordinates (x, y, z) for all 21 finger joints
            for lm in hand_landmarks.landmark:
                landmark_data.append({
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z
                })

    # Show the UI on the video screen
    cv2.putText(image, f"Recording: {current_word.upper()}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('ASL Mocap Studio', image)

    key = cv2.waitKey(5) & 0xFF
    
    # Press 's' to SNAPSHOT and SAVE the math!
    if key == ord('s'):
        if len(landmark_data) == 21:
            filename = f"{output_folder}/letter_{current_word}.json"
            
            # Write the raw math to a JSON file
            with open(filename, 'w') as f:
                json.dump(landmark_data, f, indent=4)
                
            print(f"✅ SUCCESS: Saved 21 mathematical joints to {filename}!")
            
            # Ask for the next letter so you don't have to restart the camera
            current_word = input("Which letter is next? (or type 'quit' to stop): ").lower()
            if current_word == 'quit':
                break
        else:
            print("⚠️ Cannot save: Make sure your whole hand is clearly in the frame!")

    # Press 'q' to quit out of the video window
    elif key == ord('q'):
        break

hands.close()
cap.release()
cv2.destroyAllWindows()