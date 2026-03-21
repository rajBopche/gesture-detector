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
        background-color: #000000;
    }
    .stAppDeployButton {
        visibility: hidden;
    }
    #MainMenu {
        visibility: hidden;
    }
    header {
        background-color: #000000 !important;
    }
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


random_titles = [
    "Cascade Flux",
    "Nebula Drift",
    "Prismatic Surge",
    "Quantum Bloom",
    "Aurora Angle",
    "Vertex Pulse",
    "Echo Tide",
    "Vortex Whisper",
]

mock_cards = [
    {
        "id": "card_1",
        "title": random.choice(random_titles),
        "description": "Detect left-to-right swipe gestures and trigger navigation actions.",
        "image": "https://picsum.photos/seed/swipe-left/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_2",
        "title": random.choice(random_titles),
        "description": "Handle right-to-left swipes to reveal controls and options.",
        "image": "https://picsum.photos/seed/swipe-right/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_3",
        "title": random.choice(random_titles),
        "description": "Support pinch-to-zoom gesture recognition for detail inspection.",
        "image": "https://picsum.photos/seed/pinch-zoom/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_4",
        "title": random.choice(random_titles),
        "description": "Long-press and hold gestures for context menus and tools.",
        "image": "https://picsum.photos/seed/hold-press/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_11",
        "title": random.choice(random_titles),
        "description": "Detect left-to-right swipe gestures and trigger navigation actions.",
        "image": "https://picsum.photos/seed/swipe-left/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_21",
        "title": random.choice(random_titles),
        "description": "Handle right-to-left swipes to reveal controls and options.",
        "image": "https://picsum.photos/seed/swipe-right/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_31",
        "title": random.choice(random_titles),
        "description": "Support pinch-to-zoom gesture recognition for detail inspection.",
        "image": "https://picsum.photos/seed/pinch-zoom/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_41",
        "title": random.choice(random_titles),
        "description": "Long-press and hold gestures for context menus and tools.",
        "image": "https://picsum.photos/seed/hold-press/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_111",
        "title": random.choice(random_titles),
        "description": "Detect left-to-right swipe gestures and trigger navigation actions.",
        "image": "https://picsum.photos/seed/swipe-left/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_211",
        "title": random.choice(random_titles),
        "description": "Handle right-to-left swipes to reveal controls and options.",
        "image": "https://picsum.photos/seed/swipe-right/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_311",
        "title": random.choice(random_titles),
        "description": "Support pinch-to-zoom gesture recognition for detail inspection.",
        "image": "https://picsum.photos/seed/pinch-zoom/180/120",
        "button": "Try Now",
    },
    {
        "id": "card_411",
        "title": random.choice(random_titles),
        "description": "Long-press and hold gestures for context menus and tools.",
        "image": "https://picsum.photos/seed/hold-press/180/120",
        "button": "Try Now",
    },
]

for card_data in mock_cards:
    with st.container():
        c1, c2, c3 = st.columns([1, 3, 1], gap="small")

        with c1:
            st.markdown(
                f"""
                <div class='card-image'><img src='{card_data['image']}' alt='{card_data['title']}' /></div>
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
            if st.button(card_data["button"], key=card_data["id"], type="primary"):
                st.switch_page("camera.py")

    st.markdown(
        "<hr style='border: .5px solid rgba(148, 163, 184, 0.35);'>",
        unsafe_allow_html=True,
    )
