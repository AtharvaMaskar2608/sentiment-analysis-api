from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import io
from dotenv import load_dotenv
from utils import *

# Load environment variables
load_dotenv()

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

        print(audio_transcripts)

        # Save or process the transcript as needed
        # For example, save to a database or file

    except Exception as e:
        print(f"Error processing file: {e}")

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

    print(response_data)


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


def get_audio_transcript_analysis(file_bytes: bytes, filename: str):
    try:
        file_io = io.BytesIO(file_bytes)
        file_io.name = filename

        agent_name = ""
        # Generate transcript
        transcription = client.audio.translations.create(
            model="whisper-1",
            file=file_io
        )
        
        audio_transcripts = transcription.text

        # Generate summary
        summary = generate_sumary(audio_transcripts, agent_name)

        # Greeting score
        greeting_score = check_greeting(audio_transcripts, summary)

        # Empathy score
        empathy_score = check_empathy(audio_transcripts, summary)

        # Closure score
        closure_score = check_closure(audio_transcripts, summary)

        # Query Type
        query_type = get_query_type(audio_transcripts)

        response_data = {
            "transcript": audio_transcripts,
            "greeting_score": greeting_score,
            "empathy_score": empathy_score,
            "closure_score": closure_score, 
            "query_type": query_type
        }


        # PUSH IT TO DATABASE. 


        print(response_data)

    except Exception as e:
        print(f"Error processing file: {e}")

@app.post("/audio-sentiment-analysis/")
async def audio_sentiment_analysis(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No selected file")

    try:
        file_bytes = await file.read()  # Asynchronously read file
        filename = file.filename

        # Add the background task
        background_tasks.add_task(get_audio_transcript_analysis, file_bytes, filename)

        return JSONResponse(
            content={"message": "Sentiment analysis started successfully"},
            status_code=201
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the server with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
