import cv2
import os
import time
import numpy as np
import mediapipe as mp

# Initialize Mediapipe Hand model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Define gestures
GESTURES = ["palm", "fist", "thumbs_up", "thumbs_down", "index", "two_fingers", "mute"]

# Base dataset directory
DATASET_DIR = "backend/gestures/ml/dataset"

# Auto-create folders
for gesture in GESTURES:
    os.makedirs(os.path.join(DATASET_DIR, gesture), exist_ok=True)

print("\n✅ Dataset folders verified/created successfully!\n")

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("❌ Cannot access webcam!")

print("🎥 Webcam ready.\n")
print("Press keys 1–7 to select gesture:")
for i, g in enumerate(GESTURES, start=1):
    print(f"{i}: {g}")
print("\nPress 'q' to quit.\n")

current_gesture = None
recording = False
save_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Draw landmarks if detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display text on window
    info = f"Gesture: {current_gesture if current_gesture else 'None'} | Saved: {save_count}" if recording else "Press a key (1–7) to choose gesture"
    cv2.putText(frame, info, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0) if recording else (0, 0, 255), 2)

    cv2.imshow("Hand Landmark Collector", frame)

    key = cv2.waitKey(1) & 0xFF

    # Quit
    if key == ord('q'):
        break

    # Select gesture keys 1–7
    if ord('1') <= key <= ord(str(len(GESTURES))):
        index = key - ord('1')
        current_gesture = GESTURES[index]
        print(f"\n👉 Selected gesture: {current_gesture}")
        input("Press Enter to start capturing...")
        print("⚡ Recording started! (Press 's' to stop)")
        recording = True
        save_count = 0

    # Stop recording
    if key == ord('s'):
        recording = False
        current_gesture = None
        print("🛑 Recording stopped.")

    # Save landmark data while recording
    if recording and results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            # Save to .npy file
            save_path = os.path.join(DATASET_DIR, current_gesture, f"{int(time.time() * 1000)}.npy")
            np.save(save_path, np.array(landmarks))
            save_count += 1

cap.release()
cv2.destroyAllWindows()
print("\n✅ Data collection finished successfully!")
