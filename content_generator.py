import google.generativeai as genai
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Configure the Gemini AI API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Set up the Gemini AI model
model = genai.GenerativeModel('gemini-pro')

def get_emoji_for_content_type(content_type):
    emoji_map = {
        "Post": ["📝", "✍️", "📊", "📈", "📰"],
        "Comment": ["💬", "🗨️", "🔔", "📢", "🗣️"],
        "Response": ["↩️", "🔁", "📨", "📤", "🔄"]
    }
    return random.choice(emoji_map.get(content_type, ["📄"]))

def get_emoji_for_tone(tone):
    emoji_map = {
        "Neutral": ["😐", "📊", "🔹"],
        "Friendly": ["😊", "👋", "🌟"],
        "Professional": ["👔", "💼", "🏢"],
        "Humorous": ["😄", "😂", "🎭"],
        "Formal": ["🎩", "📜", "🖋️"]
    }
    return random.choice(emoji_map.get(tone, ["📝"]))

def generate_content(prompt, state):
    user_interests = ", ".join(state.user_interests) if state.user_interests else "general topics"
    content_emoji = get_emoji_for_content_type(state.content_type)
    tone_emoji = get_emoji_for_tone(state.tone)
    
    full_prompt = f"""
    Generate a {state.content_type} with the following characteristics:
    - Tone: {state.tone} {tone_emoji}
    - Max Length: {state.max_length} characters
    - Topic: {prompt}
    - User Interests: {user_interests}

    Please ensure the content is:
    1. Engaging and relevant to the user's interests
    2. Coherent and contextually appropriate
    3. Compliant with community guidelines (no inappropriate or harmful content)
    4. Formatted for easy reading (use paragraphs, bullet points, or numbered lists as appropriate)
    5. Includes relevant emojis throughout the content to enhance readability and engagement

    Start the {state.content_type} with the emoji {content_emoji}.
    """
    response = model.generate_content(full_prompt)
    return response.text