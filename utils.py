import streamlit as st

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'user_interests' not in st.session_state:
        st.session_state.user_interests = []

emoji_map = {
    "Post": "📝",
    "Comment": "💬",
    "Response": "↩️",
    "Neutral": "😐",
    "Friendly": "😊",
    "Professional": "👔",
    "Humorous": "😄",
    "Formal": "🎩"
}