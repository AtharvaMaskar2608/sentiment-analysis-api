from fastapi import FastAPI, UploadFile, BackgroundTasks
from starlette.responses import JSONResponse
import asyncio
import time

app = FastAPI()

def process_file(file_path: str):
    # Simulate a time-consuming file processing task
    time.sleep(10)  # Replace with actual processing logic
    # Append to database (not shown here)
    print(f"File {file_path} processed and saved to the database.")

@app.post("/upload/")
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    file_location = file
    
    content = await file.read()

    # Start the file processing in the background
    background_tasks.add_task(process_file, file_location)
    
    # Immediately respond to the user
    return JSONResponse(content={"message": "File uploaded successfully. Processing in the background."})

# To run the application, use: uvicorn filename:app --reload
