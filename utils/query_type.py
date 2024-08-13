from openai import OpenAI
import json
client = OpenAI()
import os

QUERY_TYPE_PATH = "storage/type-query.json"

def get_query_type(transcript: str) -> str:
    """
    Description:
        - This function takes the transcript and returns which query type it belongs to. 
    parameters: 
        - transcript (str): Transcript of the call
    returns:
        - query type        
    """

    query_types = []

    with open(QUERY_TYPE_PATH, 'r') as jsonFile:
        query_types = json.load(jsonFile)
    
    system_prompt = f"""You are a professional hindi sales call analyzer. You will be given a hindi transcript, you have to classify the transcript into one of the following queries. Check the query name and it's description and return only the name of the query that describes the call. Do not return any justification or other text. {query_types}"""

    user_prompt = f"{transcript}. Classifiy the given transcript into a query type"

    completion = client.chat.completions.create(
        temperature=0,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return completion.choices[0].message.content

def get_audio_urls(folder_path: str):
    """
    Description:
        - This function returns the parth of all the files in a folder
    parameters:
        - folder_path (str): Path of the folder

    returns:
        - audio_urls (arr): Array of all audio urls in a folder        
    """

    # List to store file paths
    file_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    return file_paths