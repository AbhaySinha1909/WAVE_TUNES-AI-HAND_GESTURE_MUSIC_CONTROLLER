import cv2
import numpy as np
import time
import tensorflow as tf
from tensorflow import keras
from backend.music_control.music_controller import MusicController
import requests

def send_gesture_to_backend(gesture):
    """Sends the detected gesture string to the backend API."""
    try:
        url = "http://127.0.0.1:8000/api/gestures/update/"
        requests.post(url, json={"gesture": gesture})
    except Exception as e:
        print("⚠️ Failed to send gesture:", e)

# Load trained model
model = keras.models.load_model('backend/gestures/ml/keras_model.h5')
print("✅ Gesture model loaded successfully!")

# Gesture class names
classes = ["palm", "fist", "thumbs_up", "thumbs_down", "index", "two_fingers", "mute"]

# Initialize Music Controller
music = MusicController()

# Webcam setup
cap = cv2.VideoCapture(0)

# Parameters for smoothing
CONFIDENCE_THRESHOLD = 0.85
SMOOTH_FRAMES = 3  # gesture must be consistent for 3 frames
cooldown = 1.5  # seconds between actions

prev_gesture = None
gesture_counter = 0
last_action_time = 0

print("🎬 Starting real-time gesture music control...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    img = cv2.resize(frame, (224, 224))
    img = np.expand_dims(img / 255.0, axis=0)

    # Predict gesture
    prediction = model.predict(img, verbose=0)
    class_index = np.argmax(prediction)
    confidence = prediction[0][class_index]
    gesture = classes[class_index]

    # Display on screen
    cv2.putText(frame, f"{gesture} ({confidence*100:.1f}%)", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if confidence > CONFIDENCE_THRESHOLD else (0,0,255), 2)

    # Smoothing: gesture must be detected consistently
    if confidence > CONFIDENCE_THRESHOLD:
        if gesture == prev_gesture:
            gesture_counter += 1
        else:
            prev_gesture = gesture
            gesture_counter = 1
    else:
        gesture_counter = 0
        prev_gesture = None

    # Trigger action if gesture held consistently and cooldown passed
    if gesture_counter >= SMOOTH_FRAMES and (time.time() - last_action_time) > cooldown:
        last_action_time = time.time()
        gesture_counter = 0
        print(f"🖐 Detected Gesture: {gesture}")
        send_gesture_to_backend(gesture)


        if gesture == "palm":
            music.play_music()
        elif gesture == "fist":
            music.stop_music()
        elif gesture == "thumbs_up":
            music.volume_up()
        elif gesture == "thumbs_down":
            music.volume_down()
        elif gesture == "index":
            music.next_track()
        elif gesture == "two_fingers":
            music.prev_track()
        elif gesture == "mute":
            music.mute_music()

    # Show webcam feed
    cv2.imshow("Gesture Music Controller", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()