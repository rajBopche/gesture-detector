import cv2
import mediapipe as mp
import pyttsx3
import joblib

# ---------------- TTS Setup ----------------
engine = pyttsx3.init()
last_spoken = ""

# Prediction smoothing
prediction_history = []
history_size = 10

# Load trained AI model
model = joblib.load("gesture_model.pkl")

# ---------------- MediaPipe Setup ----------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)

# ---------------- Camera Setup ----------------
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ---------------- Main Loop ----------------
while True:

    success, frame = cap.read()

    if not success:
        print("Camera not detected")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)
    pose_result = pose.process(rgb_frame)

    # ----------- Draw Pose Landmarks -----------
    if pose_result.pose_landmarks:
        mp_draw.draw_landmarks(
            frame,
            pose_result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    # ----------- Hand Detection -----------
    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                mp_draw.DrawingSpec(color=(255,0,0), thickness=2)
            )

            lm = hand_landmarks.landmark
            landmarks = []

            # ----------- Normalize landmarks (IMPORTANT) -----------
            for lm_point in lm:
                landmarks.append(lm_point.x - lm[0].x)
                landmarks.append(lm_point.y - lm[0].y)
                landmarks.append(lm_point.z - lm[0].z)

            if len(landmarks) > 0:

                # ----------- Prediction -----------
                prediction = model.predict([landmarks])[0]

                # ----------- Prediction smoothing -----------
                prediction_history.append(prediction)

                if len(prediction_history) > history_size:
                    prediction_history.pop(0)

                gesture_text = max(set(prediction_history), key=prediction_history.count)

                # ----------- Show Gesture Text -----------
                cv2.putText(
                    frame,
                    f"Gesture: {gesture_text}",
                    (10,140),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0,255,255),
                    3
                )

                # ----------- Voice Output -----------
                if gesture_text != last_spoken:
                    engine.say(gesture_text)
                    engine.runAndWait()
                    last_spoken = gesture_text

    # ----------- Show Output -----------
    cv2.imshow("Two-Hand Detection - Sign Language Project", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---------------- Close Camera ----------------
cap.release()
cv2.destroyAllWindows()