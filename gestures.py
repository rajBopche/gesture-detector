import base64

import streamlit as st
import random

st.set_page_config(page_title="Gesture Cards", layout="wide")

st.markdown(
    """
<style>
    .stApp {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        background-color: #0f1116;
    }
    .stAppDeployButton {
        visibility: hidden;
    }
    #MainMenu {
        visibility: hidden;
    }
    header {
        background-color: #0f1116 !important;
    }
    .stButton button {
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        background: #0f1116;
        color: var(--text);
        font-weight: 600;
        padding: 0.65rem 1.1rem;
    }
    .stButton button:hover {
        background: rgba(124, 92, 255, 0.32);
    }
    [data-testid="stSidebarNavItems"] span {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 500;
        color: #f0f2f6;
    }
.card-container {
    background: #ffffff;
    border-radius: 14px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    padding: 14px;
    margin-bottom: 18px;
    border: 1px solid rgba(100, 116, 139, 0.15);
}
.card-row {
    display: flex;
    gap: 12px;
    align-items: center;
}
.card-image img {
    width: 100%;
    height: auto;
    border-radius: 10px;
    object-fit: cover;
    border: 1px solid rgba(148, 163, 184, 0.4);
}
.card-content {
    padding: 2px 0;
}
.card-title {
    margin: 0;
    color: #ffffff;
    font-size: 1.05rem;
    font-weight: 500;
}
.card-desc {
    color: #ffffff;
    margin: 6px 0 0;
    font-size: 0.94rem;
    line-height: 1.4;
}
.card-action {
    display: flex;
    justify-content: center;
}
</style>
""",
    unsafe_allow_html=True,
)


gesture_titles = [
    "All The Best",
    "Loser",
    "Sorry",
    "Fine",
    "Call Me",
    "Hi",
]

mock_cards = [
    {
        "id": "card_1",
        "title": gesture_titles[0],
        "description": "The most common hand sign used to wish someone all the best, often used to symbolise luck or hope",
        "image": "./both_thumbs_up.jpg",
        "button": "Try Now",
    },
    {
        "id": "card_2",
        "title": gesture_titles[1],
        "description": "You extend both arms and point both thumbs toward the ground. A double thumbs-down is the ultimate universal signal for double failure or total disapproval",
        "image": "./loser_down.avif",
        "button": "Try Now",
    },
    {
        "id": "card_3",
        "title": gesture_titles[2],
        "description": "Holding your ears with both hands (often while crossing your arms or slightly squatting) is a classic gesture used to express sincere apology, regret, or asking for forgiveness.",
        "image": "./sorry.jpg",
        "button": "Try Now",
    },
    {
        "id": "card_4",
        "title": gesture_titles[3],
        "description": "A single thumbs up is the most common hand gesture for fine, signifying that everything is under control, approved, or understood. It is a versatile all-purpose sign used to replace verbal phrases like sounds good, okay, or got it",
        "image": "./fine_thumbs_up.png",
        "button": "Try Now",
    },
    {
        "id": "card_5",
        "title": gesture_titles[4],
        "description": "The sign is made by extending your thumb and little finger while keeping your middle three fingers curled into your palm, then holding it up to your ear. It is a classic, intuitive gesture that mimics the shape of an old-school telephone receiver",
        "image": "./call_me.jpg",
        "button": "Try Now",
    },
    {
        "id": "card_6",
        "title": gesture_titles[5],
        "description": "Raising your hand to about shoulder height and moving it side-to-side. It’s the universal hello or hi often used when you're passing someone quickly",
        "image": "./hi.avif",
        "button": "Try Now",
    },
]


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


for card_data in mock_cards:
    with st.container():
        c1, c2, c3 = st.columns([1, 3, 1], gap="small")

        with c1:
            st.markdown(
                f"""
                <div class='card-image'><img src='data:image/png;base64,{get_base64_image(card_data['image'])}' alt='{card_data['title']}' /></div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class='card-content'>
                    <div class='card-title'>{card_data['title']}</div>
                    <div class='card-desc'>{card_data['description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            if st.button(card_data["button"], key=card_data["id"]):
                st.switch_page("camera.py")

    st.markdown(
        "<hr style='border: .5px solid rgba(148, 163, 184, 0.35);'>",
        unsafe_allow_html=True,
    )
