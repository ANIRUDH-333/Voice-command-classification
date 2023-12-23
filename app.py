from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Google API
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-pro')

# Create text input for user message
# prompt = st.text_input("Message", key="user_input")
system_prompt = "You are a best classifier for 4 classes. Based on the context, you have to classify if it FORWARD, BACKWARD, RIGHT, LEFT. Finally, your response should only be a one word which is one of these: FORWARD, BACKWARD, RIGHT, LEFT. The following is the content on which you have to classify:"
prompt = st.text_input("Where do you want to move")

# Create button for user to submit their message
btn = st.button("Ask")
# st.text(system_prompt+prompt)

if btn:
    response = model.generate_content(system_prompt+prompt)
    # Display the generated content in a text area
    st.text(response.text)
