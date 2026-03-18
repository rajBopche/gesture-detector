import cv2
import mediapipe as mp
import os
import pandas as pd

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.7
)

dataset_path = "dataset"

data = []
labels = []

for gesture in os.listdir(dataset_path):

    folder = os.path.join(dataset_path, gesture)

    for img in os.listdir(folder):

        path = os.path.join(folder, img)

        image = cv2.imread(path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb)

        left_hand = None
        right_hand = None

        if result.multi_hand_landmarks and result.multi_handedness:

            for hand_landmarks, hand_info in zip(
                result.multi_hand_landmarks,
                result.multi_handedness
            ):

                lm = hand_landmarks.landmark
                landmarks = []

                for p in lm:
                    landmarks.append(p.x - lm[0].x)
                    landmarks.append(p.y - lm[0].y)
                    landmarks.append(p.z - lm[0].z)

                label = hand_info.classification[0].label

                if label == "Left":
                    left_hand = landmarks
                else:
                    right_hand = landmarks

            # Only save if both hands detected
            if left_hand is not None and right_hand is not None:

                full_landmarks = left_hand + right_hand

                data.append(full_landmarks)
                labels.append(gesture)

df = pd.DataFrame(data)
df["label"] = labels

df.to_csv("gesture_dataset.csv", index=False)

print("Two-hand dataset created successfully")