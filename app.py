from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import roslibpy

# Load environment variables
load_dotenv()

# Configure the Google API
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini Pro model
model = genai.GenerativeModel('gemini-pro')

# Speech to text function
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)

def publish(data):
    client = roslibpy.Ros(host='localhost', port=9090)
    client.run()

    talker = roslibpy.Topic(client, '/keyboard_input', 'std_msgs/String')
    talker.publish(roslibpy.Message({'data': data}))


system_prompt = "You are a best classifier for 4 classes. Based on the context, you have to classify if it FORWARD, BACKWARD, RIGHT, LEFT. Finally, your response should only be a one word which is one of these: FORWARD, BACKWARD, RIGHT, LEFT. The following is the content on which you have to classify:"
# Create button for voice command
if st.button('Press and Speak'):
    st.write('Listening...')
    audio_text = speech_to_text()
    st.write("You said: ", audio_text)

    # Use the transcribed text
    response = model.generate_content(system_prompt + audio_text)
    # Display the generated content in a text area
    
    st.text(f"Publishing : {response.text}")
    
    if response.text == "FORWARD":
        publish("up")
    elif response.text == "BACKWARD":
        publish("down")
    elif response.text == "RIGHT":
        publish("right")
    elif response.text == "LEFT":
        publish("left")
    else:
        st.text("Can you come again...")


# Initialize session states
if 'show_input' not in st.session_state:
    st.session_state['show_input'] = False

# When the user clicks the "Write something" button
if st.button("Write something"):
    st.session_state['show_input'] = True

# Display the input field if 'show_input' is True
if st.session_state['show_input']:
    # Use a different key for the text input widget
    user_input = st.text_input("Write here!", key="input")

    # When the user clicks the "Ask" button
    if st.button("Ask"):
        # Check if there is user input to process
        if user_input:
            # Display the entered text
            st.text("You said: " + user_input)

            # Generate a response from the model
            response = model.generate_content(system_prompt + user_input)

            # Display the model's response
            st.text(response.text)
        else:
            # Inform the user to enter some text first
            st.warning("Please enter some text before asking.")