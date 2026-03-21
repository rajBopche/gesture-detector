import base64
import os

import cv2
import joblib
import mediapipe as mp
import numpy as np
import pyttsx3
import streamlit as st

# ---------------- Voice Setup ----------------
engine = pyttsx3.init()

# ---------------- Page Setup ----------------
st.set_page_config(
    page_title="AI Sign Language Assistant",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------- CSS (dark / modern) ----------------
st.markdown(
    """
    <style>
    :root {
        --bg: #0b1220;
        --card: rgba(255, 255, 255, 0.05);
        --card-border: rgba(255, 255, 255, 0.12);
        --text: #f2f7ff;
        --muted: rgba(242, 247, 255, 0.67);
        --accent: #7c5cff;
        --accent2: #3bf0ff;
    }

    .stApp {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background-color: #000000;
    }

    .header {
        text-align: center;
        padding: 1.5rem 0 0.75rem;
    }

    .header h1 {
        font-size: 2.6rem;
        margin: 0;
        letter-spacing: 0.02em;
        background: linear-gradient(90deg, var(--accent), var(--accent2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .header p {
        margin: 0.35rem auto 0;
        max-width: 680px;
        background: linear-gradient(90deg, var(--accent), var(--accent2));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.05rem;
        line-height: 1.55;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 0.22rem 0.7rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.16);
        background: rgba(50, 60, 100, 0.2);
        color: var(--text);
        font-weight: 600;
        font-size: 0.92rem;
    }

    .pill span {
        opacity: 0.8;
    }
    
    .stAppDeployButton {
        visibility: hidden;
    }

    .stCheckbox > div {
        gap: 0.45rem;
    }

    .stCheckbox label {
        font-size: 1rem;
        font-weight: 600;
    }
    
    #MainMenu {
        visibility: hidden;
    }
    
    footer {
        visibility: hidden;
    }
        
    header {
        visibility: hidden
    }
    
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}


    .stButton button {
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        background: rgba(124, 92, 255, 0.15);
        color: var(--text);
        font-weight: 600;
        padding: 0.65rem 1.1rem;
    }

    .stButton button:hover {
        background: rgba(124, 92, 255, 0.32);
    }

    .stMarkdown h2 {
        font-size: 1.25rem;
        margin: 0.5rem 0 0.65rem;
    }

    .stMarkdown p {
        color: var(--muted);
    }

    .stMarkdown ul {
        padding-left: 1.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- State Setup ----------------
if "last_spoken" not in st.session_state:
    st.session_state.last_spoken = ""

if "camera_running" not in st.session_state:
    st.session_state.camera_running = False

# ---------------- Model ----------------
model = joblib.load("gesture_model.pkl")

# ---------------- Header ----------------
with st.container():
    st.markdown(
        """
        <div class='header'>
            <h1>🤖 AI Sign Language Assistant</h1>
            <p>Point your hands at the camera and let the model translate sign language into text (and speech).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------- Layout ----------------
left_spacer, main_col, right_spacer = st.columns([1, 8, 1])

with main_col:
    with st.container():
        # Controls + status
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            label = "Stop Camera" if st.session_state.camera_running else "Start Camera"
            if st.button(label, type="primary", icon="📷", use_container_width=True):
                st.session_state.camera_running = not st.session_state.camera_running
                st.rerun()  # Forces an immediate refresh to update the UI
        with btn_col2:
            if st.button(
                "Gestures", type="secondary", icon="👋", use_container_width=True
            ):
                st.switch_page("gestures.py")

    frame_container = st.container()

    with frame_container:
        frame_placeholder = st.empty()

# ---------------- MediaPipe Setup ----------------
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

pose = mp_pose.Pose()

# ---------------- Camera ----------------
if st.session_state.camera_running:
    camera = cv2.VideoCapture(0)

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while st.session_state.camera_running:
        success, frame = camera.read()
        if not success:
            st.error("Camera not detected")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        hand_result = hands.process(rgb)
        pose_result = pose.process(rgb)

        gesture = ""

        # ---------------- Draw Half Body ----------------
        if pose_result.pose_landmarks:
            mp_draw.draw_landmarks(
                frame, pose_result.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

        left_hand = None
        right_hand = None

        # ---------------- Hand Detection ----------------
        if hand_result.multi_hand_landmarks and hand_result.multi_handedness:
            for hand_landmarks, hand_info in zip(
                hand_result.multi_hand_landmarks, hand_result.multi_handedness
            ):
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                label = hand_info.classification[0].label
                lm = hand_landmarks.landmark
                landmarks = []

                for p in lm:
                    landmarks.append((p.x - lm[0].x) * 100)
                    landmarks.append((p.y - lm[0].y) * 100)
                    landmarks.append((p.z - lm[0].z) * 100)

                if label == "Left":
                    left_hand = landmarks
                else:
                    right_hand = landmarks

        # ---------------- AI Prediction ----------------
        if left_hand is not None and right_hand is not None:
            full_landmarks = left_hand + right_hand

            prediction = model.predict([full_landmarks])
            gesture = prediction[0]

            if hasattr(model, "predict_proba"):
                confidence = np.max(model.predict_proba([full_landmarks]))
            else:
                confidence = 1.0

            cv2.putText(
                frame,
                f"{gesture} ({confidence:.2f})",
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            if gesture != st.session_state.last_spoken:
                engine.say(gesture)
                engine.runAndWait()

        frame_placeholder.image(frame, channels="BGR")

    camera.release()
