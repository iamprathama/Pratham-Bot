from dotenv import load_dotenv 
load_dotenv()

import streamlit as st
import os
import time
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
import base64
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("gemini-1.5-pro")

def my_output(query) ->str:
    response=model.generate_content(query)
    return response.text

def text_to_speech(text):
    tts = gTTS(text)
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)  # Removed incorrect 'format' argument
    audio_fp.seek(0)
    audio_base64 = base64.b64encode(audio_fp.read()).decode()
    return f"data:audio/mp3;base64,{audio_base64}"

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
         return "Error with speech recognition service."
st.set_page_config(page_title="Pratham Bot", page_icon="🤖", layout="centered")


with st.sidebar:
       st.title("⚙️ Settings")
       st.write("Customize your chatbot experience.")
       speed = st.slider("Response Speed", 5, 20, 10)
       st.write("Adjust the delay before response.")
       st.markdown("""
        <h1 style='text-align: center; color: #4CAF50;'>🤖 Pratham_Bot</h1>
        <p style='text-align: center; color: grey;'>Your AI assistant powered by Gemini!</p>
        <hr>
        """, unsafe_allow_html=True) 
st.balloons()

if st.button("🎤 Speak Now"):
    user_input = speech_to_text()
    st.text(f"Recognized Text: {user_input}")
else:user_input = st.text_input("Enter your query:", key="input")
submit=st.button("ask your query")

if submit :
    response=my_output(user_input)
    with st.spinner('wait for it'):
     time.sleep(10)
    st.subheader("the response is=")
    st.write(response)
    audio_link = text_to_speech(response)
    st.markdown(f'<audio controls><source src="{audio_link}" type="audio/mp3"></audio>', unsafe_allow_html=True)


