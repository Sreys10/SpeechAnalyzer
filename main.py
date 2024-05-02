import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pygame
from io import BytesIO
import google.generativeai as genai


# Set page title and favicon as the first Streamlit command
st.set_page_config(page_title="Speech Analyzer", page_icon=":microphone2:")

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

# Your app code here

# Set page subheader
# st.subheader("Hey there \U0001F44B \U0001F603 please click the \"Speak\" button and say something, I will check and correct your grammar \U0001F609.")

# Set up columns for buttons
col1, col2, col3, col4, col5 = st.columns(5)

st.markdown(
    """
    <style>
        body {
            background-color: #ffffff;
        }
        .stButton>button {
            border: none;
            color: white;
            padding: 14px 28px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 17px;
            margin: 4px 2px;
            transition-duration: 0.4s;
            cursor: pointer;
            background-color: white; 
            color: black; 
            border: 2px solid #008CBA;
        }
        .stButton>button:hover {
            background-color: #008CBA;
            color: white;
        }
        .stTextInput>input {
            transition-duration: 0.3s;
            border-color: #008CBA;
            border-width: 2px;
        }
        .stTextInput>input:focus {
            border-color: #005f73;
            outline: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def footer():
    footer_style = """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #000000;
        color: #8c8c8c;
        text-align: center;
        padding: 10px;
        font-size: 16px;
    }
    .footer hr {
        margin: 10px 0;
        border: none;
        border-top: 1px solid #eee;
    }
    .footer p {
        margin: 5px 0;
    }
    </style>
    """
    st.markdown(footer_style, unsafe_allow_html=True)

    team_names = [
        "Niranjan Chirde",
        "Shreyas Deshmukh",
        "Swanand Deshpande",
        "Devyani Deshpande",
        "Beryl Dsouza"
    ]
    team_str = " | ".join(team_names)  # Join the names with a separator

    footer_html = f"""
    <div class="footer">
        <hr>
        <p>Created by: {team_str}</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


# Call the function to render the footer
footer()

# Initialize Google Generative AI API with your API key
genai.configure(api_key="AIzaSyD8moHL0Cvj0yBCQX1z2kXXddGGz8qjwDY")

# Set page background color
st.markdown(
    """
    <style>
        body {
            background-color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Set page header
st.header("Speech Analyzer")

# Set page subheader
st.subheader("Hey there 🤖😊 please click the \"Speak\" button and say something, I will check and correct your grammar 🤓.")

# Set up columns for buttons
col1, col2, col3, col4, col5 = st.columns(5)

# Set up speak button
isspeak = col3.button("Speak")

# Set up pygame for audio playback
pygame.init()
pygame.mixer.init()

# Set up function for speech recognition and correction
def recognize_speech():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    mic = sr.Microphone()

    with mic as source:
        st.write("Please wait, I'm listening...")
        audio = recognizer.adjust_for_ambient_noise(source, duration=0.2)
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        st.write("Analyzing your speech...")
        try:
            text = recognizer.recognize_google(audio).lower()
            corrected_text = correct_text_with_google(text)
            st.markdown("## Result:")
            speak(corrected_text)
            st.success(f"Corrected text: {corrected_text}")
            st.error(f"What you said: {text}")
            #speak(text)

            st.markdown(
                """
                <style>
                .result-gif {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-top: 50px; /* Adjust the margin-top as needed */
                    height: 100px;
                }
                </style>
                <div class="result-gif">
                    <img src="https://gifdb.com/images/high/correct-thats-right-donald-trump-meme-a0hr3ldxmngay359.gif" width="30%" />
                </div>
                """,
                unsafe_allow_html=True
            )

        except sr.UnknownValueError:
            st.write("Speak again please")
        except sr.RequestError:
            st.write("Speech Service down")

# Set up function for audio playback
def speak(text, language='en'):
    tts = gTTS(text, lang=language)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    pygame.mixer.music.load(mp3_fp)
    pygame.mixer.music.play()

# Function to correct text using Google Generative AI API
def correct_text_with_google(text):
    defaults = {
        'model': 'models/text-bison-001',
        'temperature': 0.4,
        'candidate_count': 4,
        'top_k': 40,
        'top_p': 0.95,
        'max_output_tokens': 1024,
    }
    prompt = "Rewrite the following sentence and fix any grammar issues.\n\n" + text

    response = genai.generate_text(
        **defaults,
        prompt=prompt
    )
    print(response.result)
    return response.result

# Display speak button and call speech recognition function when clicked
if isspeak:
    recognize_speech()




