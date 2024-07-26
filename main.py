import streamlit as st
from content_generator import generate_content
from content_moderator import moderate_content
from utils import load_css, initialize_session_state

# Initialize Streamlit page configuration
st.set_page_config(
    page_title="AI Content Manager",
    page_icon="🤖",
    layout="wide"
)

# Load custom CSS
load_css("styles.css")

# Initialize session state
initialize_session_state()

if st.button('Back to Sentient Social Media'):
    st.markdown("[Sentient Social](https://sentient-social.onrender.com)")
# Main app layout
st.title("AI Content Manager")
st.subheader("Generate and Moderate Content with AI")

# Sidebar
st.sidebar.header("Settings")
st.session_state.content_type = st.sidebar.selectbox("Content Type", ["Post", "Comment", "Response"])
st.session_state.tone = st.sidebar.selectbox("Tone", ["Neutral", "Friendly", "Professional", "Humorous", "Formal"])
st.session_state.max_length = st.sidebar.slider("Max Length", 50, 500, 250)
st.session_state.strictness = st.sidebar.slider("Moderation Strictness", 0, 100, 50)
st.session_state.categories = st.sidebar.multiselect("Moderation Categories", 
    ["Profanity", "Hate Speech", "Violence", "Adult Content", "Spam", "Misinformation"])

# User interests
st.sidebar.subheader("User Interests")
interests = st.sidebar.text_area("Enter user interests (comma-separated)")
st.session_state.user_interests = [interest.strip() for interest in interests.split(",")] if interests else []

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Content Generation", "Content Moderation", "History", "Analytics"])

with tab1:
    st.header("Generate Content")
    user_prompt = st.text_area("Enter a prompt for content generation:")
    if st.button("Generate Content"):
        if user_prompt:
            with st.spinner("Generating content..."):
                generated_content = generate_content(user_prompt, st.session_state)
            st.subheader("Generated Content:")
            st.write(generated_content)
            st.session_state.history.append(("Generated", generated_content))
            st.success("Content generated successfully!")
        else:
            st.warning("Please enter a prompt.")

with tab2:
    st.header("Moderate Content")
    user_content = st.text_area("Enter content to moderate:")
    if st.button("Moderate Content"):
        if user_content:
            with st.spinner("Moderating content..."):
                moderation_result = moderate_content(user_content, st.session_state)
            st.subheader("Moderation Result:")
            st.write(moderation_result)
            st.session_state.history.append(("Moderated", user_content, moderation_result))
            st.info("Content moderated. Check the results above.")
        else:
            st.warning("Please enter content to moderate.")

with tab3:
    st.header("History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"Item {len(st.session_state.history) - i}"):
                if item[0] == "Generated":
                    st.subheader("Generated Content")
                    st.write(item[1])
                else:
                    st.subheader("Moderated Content")
                    st.write("Original:", item[1])
                    st.write("Result:", item[2])
    else:
        st.write("No history yet. Start generating or moderating content!")

with tab4:
    st.header("Analytics")
    st.subheader("Content Generation Stats")
    generation_count = sum(1 for item in st.session_state.history if item[0] == "Generated")
    st.write(f"Total content generated: {generation_count}")

    st.subheader("Moderation Stats")
    moderation_count = sum(1 for item in st.session_state.history if item[0] == "Moderated")
    st.write(f"Total content moderated: {moderation_count}")

    if moderation_count > 0:
        violations = sum(1 for item in st.session_state.history if item[0] == "Moderated" and "violates" in item[2].lower())
        violation_rate = (violations / moderation_count) * 100
        st.write(f"Violation rate: {violation_rate:.2f}%")

    st.subheader("Most Used Content Type")
    content_type_counts = {}
    for item in st.session_state.history:
        if item[0] == "Generated":
            content_type = item[1].split()[0]  # Assuming the content type is the first word
            content_type_counts[content_type] = content_type_counts.get(content_type, 0) + 1
    if content_type_counts:
        most_used = max(content_type_counts, key=content_type_counts.get)
        st.write(f"Most used content type: {most_used}")

# Footer
st.markdown("---")
st.markdown("Powered by Gemini AI")
