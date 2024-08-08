import streamlit as st
import pandas as pd
from io import StringIO
import requests

from db import *


get_audio_sentiment_analsysis = "http://localhost:8000/audio-sentiment-analysis/"
AUDIO_FILE_URL_PATH = "https://konnect.knowlarity.com/konnect/api/v1/786824/fc8cb51d-0fbf-42ec-a41e-a24e3fdc8f05/"

AUDIO_FILE_PATH = "/home/choice/Desktop/sentiment-analysis-api/data/test.txt"

# SINGLE FILE, CAN LATER USE FOR MULTIPLE FILES.
st.title("Audio Sentiment Analysis")

with st.form("my-form"):
    uploaded_file = st.file_uploader("Choose a file")

    submit_button = st.form_submit_button("Submit")

    if submit_button and uploaded_file is not None:
        file_name = uploaded_file.name
        file_url = f"{AUDIO_FILE_URL_PATH}{file_name[:-4]}"
        audio_sentiment_template = "audio_sentiment_analysis_customersupport"
        audio_processing_status = "Not Started"

        create_entry_response = create_entry(audio_file_url=file_url, audio_sentiment_template=audio_sentiment_template, audio_processing_status=audio_processing_status)


        # Prepare the files dictionary
        files = {
            'file': (file_name, uploaded_file, 'audio/mp3'), 
        }
        # Send the POST request
        response = requests.post(get_audio_sentiment_analsysis, files=files)

        if response.status_code == 201:
            if create_entry_response:
                st.success("Sentiment Analysis process has successfully started on the file, check your dashboard for more details.")
            else:
                st.error("There was an error processing file, Please try again later.")
        
        print(response.json())