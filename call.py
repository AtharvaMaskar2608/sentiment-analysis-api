import requests

# URL of the Flask endpoint
url = 'http://127.0.0.1:5000/upload'

# Path to the audio file you want to upload
file_path = '/home/choice/Desktop/sentiment-analysis-api/data/1c64d149-313a-4d26-aff5-41ddccf34b9e.mp3'

# Open the file in binary mode
with open(file_path, 'rb') as file:
    # Prepare the files dictionary
    files = {
        'file': (file_path, file, 'audio/mp3')
    }
    # Send the POST request
    response = requests.post(url, files=files)

# Print the server's response
print(response.json())
