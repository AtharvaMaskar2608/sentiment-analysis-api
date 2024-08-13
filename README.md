# 📄 Description

The **Audio Sentiment Analysis API** is a sophisticated tool designed to evaluate call recordings by analyzing key aspects such as empathy, greeting effectiveness, and call closure quality. This API also generates detailed transcripts and concise summaries for each call recording. Tailored for customer service environments, it provides a comprehensive assessment of call quality, offering valuable insights into agent performance and customer interaction.

## Key Features

1. **Automated Transcript Generation:** Efficiently generates precise text based transcripts from call recordings.
    
2. **Call Summary Generation:** Automatically creates concise summaries from transcripts, highlighting key points and outcomes of each call.
    
3. **Greeting and Closure Scoring:** Evaluates both the effectiveness of the greeting and the quality of the call's closure, using a binary scale where 0 signifies no greeting or closure, and 1 signifies the presence of a greeting or closure.
    
4. **Empathy Evaluation:** Analyzes the emotional tone of the conversation to determine the degree of empathy conveyed.
    

---

## **Endpoints**

**BASE URL** = [https://ccanalyzer.choicetechlab.com/api](https://ccanalyzer.choicetechlab.com/api/audio-sentiment-analysis)

### 1\. Audio File Submission and Sentiment Analysis

- **Endpoint:** [/audio-sentiment-analysis](https://ccanalyzer.choicetechlab.com/api/audio-sentiment-analysis)
    
- **Method:** POST
    
- **Description:** Allows users to upload an audio file for indepth call analysis.
    

#### Requst

- **Form-Data (required)**: The audio file to be analyzed (e.g., call recording).
    

#### Response

- **Status Code:** 201
    
- **Content-Type:** `application/json`
    
- **Body:** **`{`**`message": "Sentiment analysis started successfully"`**`}`**
    

#### Example

``` bash
curl --location 'https://ccanalyzer.choicetechlab.com/api/audio-sentiment-analysis/' \
--form 'file=@"/path/to/audio_file.mp3"'

 ```

### **Notes**

**This request submits the audio file to the API for analysis and returns an immediate acknowledgment. The analysis is performed asynchronously, with the results being recorded and database fields updated in the background.**

### 2\. Fetch Records

- **Endpoint:** /fetch-records/
    
- **Method:** GET
    
- **Description:** Retrieves all records from the database.
    

#### Requst

``` bash
curl --location 'https://ccanalyzer.choicetechlab.com/api/fetch-records'

 ```

#### Response

- **Body:** **`{`**`message": "Sentiment analysis started successfully"`**`}`**
    

``` json
{
    "data": [
        {
            "audio_id": 10,
            "audio_file_url": "https://konnect.knowlarity.com/konnect/api/v1/786824/1a99dccb-6322-4171-94a2-9d4335185653",
            "audio_transcript": "<Audio Transcript>",
            "audio_summary": "<Audio Summary>",
            "audio_sentiment_template": "audio_sentiment_analysis_customersupport",
            "audio_kpis": "{\"query_type\": \"Onboarding\", \"closure_score\": 1, \"empathy_score\": 2, \"greeting_score\": \"1\"}",
            "audio_created_at": "2024-08-12T19:06:36",
            "audio_updated_at": "2024-08-12T20:02:51",
            "audio_processing_status": "Completed",
            "audio_processing_sub_status": "Completed"
        },
    ]
}

 ```