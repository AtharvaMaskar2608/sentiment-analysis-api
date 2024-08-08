from db import create_connection
import json

def create_entry(audio_file_url: str, audio_sentiment_template: str, audio_processing_status: str) -> bool:
    """
    Description: This function creates a new entry when the user uploads the file. Initially it does not input the results and only makes an entry field.

    Parameters:
        - audio_file_url (str): URL of the audio file. 
        - audio_sentiment_template (str): Template which is being used. 
        - audio_processing_status (str): Status of the audio file, it is initially set to NOT STARTED.  
    
    Returns:
        - result (bool): Returns True if entry was successfully made, returns false if there was some error
    """

    connection = create_connection()
    cursor = connection.cursor()

    insert_query = '''
    INSERT INTO audio_data (audio_file_url, audio_sentiment_template, audio_processing_status)
    VALUES (%s, %s, %s)
    '''

    data = (audio_file_url, audio_sentiment_template, audio_processing_status)
    
    try:
        cursor.execute(insert_query, data)
        connection.commit()

        print("Entry Created Successfully")
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def update_processing_status(audio_file_url: str, updated_processing_status: str) -> bool:
    """
    Description: 
        - This function updates the processing status for a particular audio file url.
    
    Parameters:
        - audio_file_url (str): URL of the audio file for which you want to update the processing status. 
        - processing_status (str): Status to which you want to upload
    
    Returns:
        - result (bool): Return True if process updated successfully, false if there was an issue. 
    """

    connection = create_connection()
    cursor = connection.cursor()

    update_query = '''
    UPDATE audio_data
    SET audio_processing_status = %s
    WHERE audio_file_url = %s
    '''

    data = (updated_processing_status, audio_file_url)
    
    try:
        cursor.execute(update_query, data)
        connection.commit()

        print("Process Updated Successfully")
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def update_sub_processing_status(audio_file_url: str, updated_sub_processing_status: str) -> bool:
    """
    Description: 
        - This function updates the Sub Processing Status for a particular audio file url.
    
    Parameters:
        - audio_file_url (str): URL of the audio file for which you want to update the processing status for. 
        - updated_sub_processing_status (str): Status to which you want to update.
    
    Returns:
        - result (bool): Return True if process updated successfully, false if there was an issue. 
    """

    connection = create_connection()
    cursor = connection.cursor()

    update_query = '''
    UPDATE audio_data
    SET audio_processing_sub_status = %s
    WHERE audio_file_url = %s
    '''

    data = (updated_sub_processing_status, audio_file_url)
    
    try:
        cursor.execute(update_query, data)
        connection.commit()

        print("Sub Process Updated Successfully")
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def update_analysis_data(audio_file_url:str, audio_transcript: str, audio_summary: str, audio_kpis: dict) -> bool:
    """
    Description:
        - According to the flow of our project, we're first creating an entry without running sentiment analysis on it. Once we have generated the results, we will update it in the database. 
    
    Parameters:
        - audio_file_url (str): URL of the audio file
        - audio_tranascript (str): Transcript of the audio file
        - audio_summary (str): Summary of the audio file
        - audio_kpis (dict): KPIs in a dictionary format. 

    Retruns:
        - result (bool): Returns true if data updated successfully, else returns false. 
    """

    connection = create_connection()
    cursor = connection.cursor()

    update_query = '''
    UPDATE audio_data
    SET audio_transcript = %s, audio_summary = %s, audio_kpis = %s
    WHERE audio_file_url = %s
    '''

    audio_kpis_json = json.dumps(audio_kpis)

    data = (audio_transcript, audio_summary, audio_kpis_json, audio_file_url)
    
    try:
        cursor.execute(update_query, data)
        connection.commit()

        print("Sub Process Updated Successfully")
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

    finally:
        cursor.close()
        connection.close()

def fetch_all_data() -> dict:
    """
    Description:
        - This function fetches all the audio files from the database. 

    Returns:
        - data (dict): All data from the database.
    """

    connection = create_connection()
    cursor = connection.cursor()

    fetch_all_query = '''SELECT * FROM audio_data'''
    try:
        cursor.execute(fetch_all_query)
        result = cursor.fetchall()

        if result:
            # Convert result to a list of dictionaries
            column_names = [description[0] for description in cursor.description]
            details = [dict(zip(column_names, row)) for row in result]
            
            return {"data": details}  # Wrap result in a dict

        else:
            return {"message": "No data found"}

    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}

    finally:
        cursor.close()
        connection.close()
