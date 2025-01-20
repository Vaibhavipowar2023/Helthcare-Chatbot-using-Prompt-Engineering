# -*- coding: utf-8 -*-
!pip install streamlit pyngrok

import os
import google.generativeai as genai
import streamlit as st
from pyngrok import ngrok

# Set up the API key
os.environ['API_KEY'] = "Use API Key "
genai.configure(api_key=os.environ['API_KEY'])

# Load the model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to interact with the healthcare chatbot
def generate_healthcare_response(user_input):
    prompt = f"""
    You are a healthcare assistant with knowledge of medical conditions, treatments, and wellness.
    - Respond only to questions related to healthcare, medicine, or wellness.
    - If the user asks about anything outside of healthcare (e.g., sports, entertainment, personal matters), politely inform them that you can only provide healthcare information.
    - Provide accurate, helpful, and concise information.
    - Always respond in a friendly and empathetic tone.

    User's question: {user_input}
    """

    # Generate response based on healthcare prompt
    response = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        generation_config={"temperature": 0.7}  # Control creativity
    )

    assistant_reply = response.candidates[0].content
    return assistant_reply

# Streamlit UI inside a container
st.markdown("""
    <style>
    .chatbox-container {
        border: 2px solid #4CAF50;
        border-radius: 15px;
        padding: 20px;
        background-color: #ffffff;
        max-width: 600px;
        margin: 0 auto;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        height: 500px;
        position: relative;
    }
    .chat-container {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        background-color: #f9f9f9;
        overflow-y: auto;
        flex-grow: 1;
        display: flex;
        flex-direction: column-reverse;
        margin-bottom: 60px;
    }
    .user-bubble {
        background-color: #4CAF50;
        color: white;
        padding: 12px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .bot-bubble {
        background-color: #e0e0e0;
        color: black;
        padding: 12px;
        border-radius: 15px;
        margin: 10px 0;
        max-width: 70%;
        float: left;
        clear: both;
    }
    .clear {
        clear: both;
    }
    .stTextInput>div {
        position: relative;
        width: 100%;
    }
    .stTextInput>div>input {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 10px;
        width: 92%;
        left: 4%;
        padding-right: 40px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 12px;
        border-radius: 10px;
        position: absolute;
        bottom: 10px;
        right: 10px;
        width: 60px;
        height: 60px;
        font-weight: bold;
        border: none;
        background-image: url('https://www.google.com/imgres?q=submit%20button%20icon%20img&imgurl=http%3A%2F%2Fwww.clker.com%2Fcliparts%2F8%2FX%2Fy%2F7%2FJ%2Fp%2Fsubmit-button.svg.hi.png&imgrefurl=http[...]
        background-size: 30px;
        background-repeat: no-repeat;
        background-position: center;
        cursor: pointer;
    }
    .title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .title-container img {
        width: 80px;
        height: 80px;
        margin-right: 0;
        border-radius: 50%;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for storing messages if it does not exist
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Create a form inside the container to make everything align together
with st.form(key="healthcare_form", clear_on_submit=False):
    st.markdown("""
        <div class="title-container">
            <h1>Healthcare Chatbot</h1>
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAABJlBMVEX///+Z6v8OFC4AAB0AACIAACUPEy4AAB8AABf//v+a6P0EDSmFyt0jNU2Z7v8JCyYhJT+Dho8AABEAABoAABUXHjIAAAAAAA/Nz9[...]
        </div>
    """, unsafe_allow_html=True)

    st.write("Ask me anything about healthcare, medicine, or wellness!")

    # Take user input
    user_input = st.text_input("You:")
    st.form_submit_button("Submit")

    # Display chat history and handle input/output
    if user_input:
        st.session_state['messages'].append({"role": "user", "text": user_input})
        response = generate_healthcare_response(user_input)
        st.session_state['messages'].append({"role": "bot", "text": response})

    # Create a container for chat messages and display them
    with st.container():
        for message in reversed(st.session_state['messages']):
            if message['role'] == "user":
                st.markdown(f"<div class='user-bubble'>{message['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-bubble'>{message['text']}</div>", unsafe_allow_html=True)
        st.markdown('<div class="clear"></div>', unsafe_allow_html=True)

# Add your ngrok authtoken to authenticate your account
!ngrok authtoken <Add token>

# Set up ngrok tunnel for Streamlit
public_url = ngrok.connect(8501)
print(f"Streamlit app is live at: {public_url}")
