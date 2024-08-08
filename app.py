import streamlit as st
import pandas as pd
from io import StringIO
import requests
get_audio_sentiment_analsysis = "http://localhost:8000/audio-sentiment-analysis/"
AUDIO_FILE_PATH = "/home/choice/Desktop/sentiment-analysis-api/data/test.txt"

# SINGLE FILE, CAN LATER USE FOR MULTIPLE FILES.
st.title("Audio Sentiment Analysis")

with st.form("my-form"):
    uploaded_file = st.file_uploader("Choose a file")

    submit_button = st.form_submit_button("Submit")

    if submit_button and uploaded_file is not None:
        AUDIO_FILE_PATH = uploaded_file.name
            # Prepare the files dictionary
        files = {
            'file': (AUDIO_FILE_PATH, uploaded_file, 'audio/mp3')
        }
        # Send the POST request
        response = requests.post(get_audio_sentiment_analsysis, files=files)

        if response.status_code == 201:
            st.success("Sentiment Analysis process has successfully started on the file, check your dashboard for more details.")

        # Print the JSON response from the FastAPI endpoint
        print(response.json())

