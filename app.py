from flask import Flask, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv
import io
from pydub import AudioSegment


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        # try:
            # Read the file into an io.BytesIO object
            file_bytes = file.read()
            file_io = io.BytesIO(file_bytes)
            file_io.name = file.filename  # Add a name attribute to mimic a file object


            # 1. GENERATE TRANSCRIPT
            transcription = client.audio.translations.create(
                model="whisper-1", 
                file=file_io
            )
            audio_transcripts = transcription.text
            
            response_data = {   
                "message": "Transcript generated successfully",
                "file_name": file.filename,
                "transcript": audio_transcripts
            }
            return jsonify(response_data), 201

        # except Exception as e:
        #     return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
