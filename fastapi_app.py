from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import io
from dotenv import load_dotenv
from utils import *

from db import *

from utils import setup_logger

# SETTING UP THE LOGGERR
logger = setup_logger()

# Load environment variables
load_dotenv()

PORT = os.getenv("PORT")
AUDIO_FILE_URL_PATH = "https://konnect.knowlarity.com/konnect/api/v1/786824/"

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str

def get_transcript(file_bytes: bytes, filename: str):
    try:
        file_io = io.BytesIO(file_bytes)
        file_io.name = filename

        # Generate transcript
        transcription = client.audio.translations.create(
            model="whisper-1",
            file=file_io
        )
        audio_transcripts = transcription.text


        # Save or process the transcript as needed
        # For example, save to a database or file

    except Exception as e:
        logger.error(f"Error generating transcripts for: {filename}")

@app.post("/generate-transcript/")
async def generate_transcript(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")

    try:
        file_bytes = await file.read()  # Asynchronously read file
        filename = file.filename

        # Add the background task
        background_tasks.add_task(get_transcript, file_bytes, filename)

        return JSONResponse(
            content={"message": "Transcript generation started successfully, Process will run in the backgroud. Should reflect in the database shortly."},
            status_code=201
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_analysis_from_transcript(transcript: str, agent_name: str):
    # Generate summary
    summary = generate_sumary(transcript, agent_name)

    # Greeting score
    greeting_score = check_greeting(transcript, summary)

    # Empathy score
    empathy_score = check_empathy(transcript, summary)

    # Closure score
    closure_score = check_closure(transcript, summary)

    # Query Type
    query_type = get_query_type(transcript)

    response_data = {
            "transcript": transcript,
            "greeting_score": greeting_score,
            "empathy_score": empathy_score,
            "closure_score": closure_score, 
            "query_type": query_type
        }

    logger.info(f"{response_data}")


@app.post("/get-analysis-from-transcript/")
async def get_analysis(data: TranscriptRequest, background_tasks: BackgroundTasks):
    transcript = data.transcript
    agent_name = ""

    try:
        background_tasks.add_task(get_analysis_from_transcript, transcript, agent_name)

        return JSONResponse(
            content={"message": "Transcript generation started successfully, Process will run in the backgroud. Should reflect in the database shortly."},
            status_code=201
        )

    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_audio_transcript_analysis(file_bytes: bytes, filename: str, audio_file_url: str):
    try:

        file_io = io.BytesIO(file_bytes)
        file_io.name = filename

        agent_name = ""

        # UPDATE SUBPROCESS TO GENERATING TRANSCRIPTS
        response = update_sub_processing_status(audio_file_url, "Generating Transcripts (1/6)")

        # Generate transcript
        transcription = client.audio.translations.create(
            model="whisper-1",
            file=file_io
        )
        
        audio_transcripts = transcription.text

        logger.info(f"Generated transcripts for file: {filename}")

        # UPDATE SUBPROCESS TO GENERATING SUMMARY
        response = update_sub_processing_status(audio_file_url, "Generating Summary (2/6)")


        # Generate summary
        summary = generate_sumary(audio_transcripts, agent_name)
        logger.info(f"Generated Summary for file: {filename}")

        # UPDATE SUBPROCESS TO GREETING SCORE
        response = update_sub_processing_status(audio_file_url, "Greeting Score (3/6)")


        # Greeting score
        greeting_score = check_greeting(audio_transcripts, summary)
        logger.info(f"Generated Greeting Score: {filename}")

        # Empathy score
        # UPDATE SUBPROCESS TO EMPATHY SCORE
        response = update_sub_processing_status(audio_file_url, "Empathy Score (4/6)")
        empathy_score = check_empathy(audio_transcripts, summary)
        logger.info(f"Generated Empathy Score: {filename}")

        # Closure score
        # UPDATE SUBPROCESS TO EMPATHY SCORE
        response = update_sub_processing_status(audio_file_url, "Closure Score (5/6)")


        closure_score = check_closure(audio_transcripts, summary)
        logger.info(f"Generated Closure Score: {filename}")
        # Query Type
        # UPDATE SUBPROCESS TO QUERY TYPE
        response = update_sub_processing_status(audio_file_url, "Query Type (6/6)")


        query_type = get_query_type(audio_transcripts)
        logger.info(f"Generated query type: {filename}")

        # UPDATE SUBPROCESS TO QUERY TYPE
        response = update_sub_processing_status(audio_file_url, "Finishing Up.")

        response_data = {
            "transcript": audio_transcripts,
            "greeting_score": greeting_score,
            "empathy_score": empathy_score,
            "closure_score": closure_score, 
            "query_type": query_type
        }


        # PUSH ALL THE VALUES TO THE DATABASE
        audio_kpis = {
            "greeting_score": greeting_score, 
            "empathy_score": empathy_score, 
            "closure_score": closure_score, 
            "query_type": query_type
        }

        response = update_analysis_data(audio_file_url, audio_transcripts, summary, audio_kpis)

        if response:
            update_subprocess_to_in_progress = update_processing_status(audio_file_url, "Completed")
            response = update_sub_processing_status(audio_file_url, "Completed")
            logger.info(f"Completed analysis for: {filename}")
        else:
            logger.error(f"Failed to generate analysis for: {filename}")
        logger.info(f"{response}")

    except Exception as e:
        update_subprocess_to_in_progress = update_processing_status(audio_file_url, "Failed")
        logger.error(f"There was an error generating analysis for: {filename}")

@app.post("/audio-sentiment-analysis/")
async def audio_sentiment_analysis(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.filename == '':
        file_url = f"{AUDIO_FILE_URL_PATH}{file.filename[:-4]}"
        logger.error(f"No file selected for file with filename: {file_url}")
        raise HTTPException(status_code=400, detail="No selected file")
    try:
        # 1. CREATE AN ENTRY
        filename = file.filename
        file_url = f"{AUDIO_FILE_URL_PATH}{filename[:-4]}"
        audio_sentiment_template = "audio_sentiment_analysis_customersupport"
        audio_processing_status = "Not Started"
        create_entry_response = create_entry(audio_file_url=file_url, audio_sentiment_template=audio_sentiment_template, audio_processing_status=audio_processing_status)

        if create_entry_response:
            logger.info(f"Entry created successfully for URL: {file_url}")
        else:
            logger.error(f"Failed to create an entry for URL: {file_url}")

        file_bytes = await file.read()  # Asynchronously read file

      
        # UPDATE THE SUBPROCESS TO "IN PROGRESS"
        update_subprocess_to_in_progress = update_processing_status(file_url, "In Progress")

        # Add the background task
        background_tasks.add_task(get_audio_transcript_analysis, file_bytes, filename, file_url)

        return JSONResponse(
            content={"message": "Sentiment analysis started successfully"},
            status_code=201
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health-check")
async def healthcheck():

        return JSONResponse(
            content={"message": "Audio Sentiment Analysis Healthcheck"},
            status_code=200
        )

# Run the server with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT, reload=True)
