import streamlit as st

# Define the pages
# Note: These strings must match the actual filenames exactly
page_1 = st.Page("camera.py", title="Camera", icon="📷", default=True)
page_2 = st.Page("gestures.py", title="Gestures", icon="🖐️")

# Initialize navigation
pg = st.navigation([page_1, page_2], position="top")

# Run the navigation
pg.run()
