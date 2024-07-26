import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini AI API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Set up the Gemini AI model
model = genai.GenerativeModel('gemini-pro')

def moderate_content(content, state):
    prompt = f"""
    Moderate the following content with a strictness level of {state.strictness}/100:

    {content}

    Check for the following categories: {', '.join(state.categories)}

    Provide a detailed analysis using the following format:
    1. Overall Assessment: (Safe/Unsafe)
    2. Detected Issues:
       - Category: [Category Name]
         Severity: (Low/Medium/High)
         Explanation: [Brief explanation]
    3. Suggested Improvements:
       - [Suggestion 1]
       - [Suggestion 2]
    4. Final Verdict: (Passes Moderation / Violates Guidelines)

    If the content is entirely appropriate, state that it passes moderation with no issues detected.
    """
    response = model.generate_content(prompt)
    return response.text