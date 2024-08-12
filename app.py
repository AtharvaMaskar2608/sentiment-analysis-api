import streamlit as st
import requests
import os 
from dotenv import load_dotenv
from db import *

load_dotenv()

get_audio_sentiment_analsysis = os.getenv("ENDPOINT")
AUDIO_FILE_URL_PATH = "https://konnect.knowlarity.com/konnect/api/v1/786824/"
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

        # create_entry_response = create_entry(audio_file_url=file_url, audio_sentiment_template=audio_sentiment_template, audio_processing_status=audio_processing_status)


        # Prepare the files dictionary
        files = {
            'file': (file_name, uploaded_file, 'audio/mpeg'), 
        }

        print("File: ", files)
        # Send the POST request
        response = requests.post(get_audio_sentiment_analsysis, files=files)
        print(response)
        if response.status_code == 201:
            if create_entry_response:
                st.success("Sentiment Analysis process has successfully started on the file, check your dashboard for more details.")
            else:
                st.error("There was an error processing file, Please try again later.")
        
        print(response.json())


# 
# 
# curl --location 'localhost:8000/audio-sentiment-analysis' --header 'Content-Type: multipart/form-data' -F 'file=@"/home/choice/Desktop/sentiment-analysis-api/data/0fc2aa8c-1cab-43a0-b8e7-f3358e0b074b.mp3"'