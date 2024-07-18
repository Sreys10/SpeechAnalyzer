import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pygame
from io import BytesIO

# Initialize pygame.mixer
pygame.init()
pygame.mixer.init()

# Function for speech synthesis and playback
def speak(text, language='en'):
    tts = gTTS(text, lang=language)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.music.load(mp3_fp)
    pygame.mixer.music.play()

# Streamlit app setup
st.set_page_config(page_title="Speech Analyzer", page_icon=":microphone:")

st.markdown(
    """
    <style>
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .image-container img {
        max-width: 50%;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="image-container">
        <img src="https://www.thestatesman.com/wp-content/uploads/2019/10/Sarfaraz.jpg">
    </div>
    """,
    unsafe_allow_html=True
)

# Set page header
st.title('Speech Analyzer')

# Set page subheader
st.subheader("Hey there 🤖😊 Please click the \"Speak\" button and say something. I will check and correct your grammar 🤓.")

# Speak button and text input
text_to_speak = st.text_input('Enter text to speak')
if st.button('Speak') and text_to_speak:
    speak(text_to_speak)

# Footer
team_names = [
    "Niranjan Chirde",
    "Shreyas Deshmukh",
    "Swanand Deshpande",
    "Devyani Deshpande",
    "Beryl Dsouza"
]
team_str = " | ".join(team_names)  # Join the names with a separator

footer_html = f"""
<div style="position: fixed; bottom: 0; width: 100%; background-color: #f0f0f0; padding: 10px; text-align: center;">
    <p>Created by: {team_str}</p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
