from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def check_greeting(transcript: str, summary: str) -> bool:
    """
    Description: This function checks if the agent has greeted the client

    parameter:
        - transcript (str): Transcript in the text format
    
    returns:
        - didGreet (bool): Returns true if the agent has greeted, returns false if the agent hasn't greeted. 
    """


    system_prompt = f"You are a hindi sales call manager, You will be given a hindi transcript and an english summary, your job is to check if the agent exchanged any greetings or pleasentaries with the customer. Sometimes the transcript does errors in labelling the agent and the customer, so if you don't find greeting by the agent check if there was any greeting in overall context of the transcript or summary. Just return a score of 0, 1 or 2 without any explanation"

    user_prompt = f"For the given transcript: {transcript}\n and summary: {summary} check if the there was any exchange of greetings/pleasentaries between the agent and the customer. Just return 1 if he does, 0 if he doesn't"


    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return completion.choices[0].message.content


def check_empathy(transcript: str, summary:str) -> int:
    """
    Description:
        - This function checks if the agent was empathetic towards the client. 
    parameter:
        - transcript (str): call transcript
    returns:
        - emapthy_score (int): Empathy score on a scale of 0 - 2. 0 - Not empathetic, 1 - Neutral, 2 - Empathetic
    """

    system_prompt = """You are a professional Indian call manager, your job is to go through the call recording transcripts in Hindi along with generated summary and ensure that the agent was empathetic towards the customer. You have to consider both the Agent's dialogues as well as the customer's dialogues and mark the call recording as 0, 1 or 2. 

    Here's how you can mark the call:

    Marking for 2 (One or more than one should match):
    - The call went smoothly. 
    - Both the agent and customer were polite, positive and communicated effectively. 
    - The customer's query was resolved satisfactorily on the call.
    - Consider overall conversation of the transcript. 

    Marking for 1:
    - The call does not satisfy any condition in 0 or 2. Explain why would you give 1 and not 0 or 2.
    
    Marking for 0 (Even if any one the below matches):
    - The call is disconnected either by the customer or the agent aprubtly without the issue being solved.
    - The agent quickly redirected the customer to email without addressing their concerns adequately on the call.
    - The call was placed on hold for an extended period (indicated in the transcript).
    - The agent's behavior was rude, impatient, uninterested, impolite.
    - Agent was interupting the customer while speaking.  
    - The agent blamed the customer or showed impatience instead of focusing on solutions.
    - The agent did not talk in the same language as the customer. that is, if the customer talked in English the agent talked in Hindi. 
    - The agent does not resolve the problem on the call. 
    - The cutomer does not receive any satisfactory solution. 
    - The agent struggles to provide clear instructions and there was confustion and misunderstanding. 
    - The customer get's frustrated because of the agent.
    - The customer seemed uninterested and lazy while answering the call.


    From the above sitatuations, mark call transcripts for any other situations you might come accross with more accuracy. Reply with only 0, 1 or 2 without giving any explanation or other text. Do not assume the tone of the speaker through transcripts and always be strict because the bar is high and any sort of impoliteness is not tollerated with the customer.
    """

    new_prompt = """Based on the following transcript between the agent and the customer you have to evaluate only Agent's dialogue's performance, considering clarity and politeness. Provide a single overall score betweein 0 or 2, where 0 is poor and 2 is good. Justify your rating with specific examples from the transcript. You can use the following criteria:

    Criteria for 0:
    - Agent was rude and mean to the customer. 
    - Agent left the customer on hold or waiting too long. 
    - Agent got frustrated and spoke too fast.
    - Agent did not talk in the language same as the customer. 
    - If the agent kept the call on hold extensively.
    - The agent got even slightly impatient and frustrated.
    - Call is empty or got disconnected without addressing or while addressing the problem midway. 
    
    Criteria for 2:
    - If the agent was very polite and understanding towards the customer, but still the customer seemed frustrated. Despite of all this the agent handled it with empathy and helped the customer. 
    - If the call had a few major problems but got solved at the end and the agent assisted the customer eventually resolving the query.
    - Or the call was smooth with few problems or no problems at all. 
    - If the agent tried to solve the problem, but it was not resolved till the end but the agent gave a solution which the user did not think of or hadn't tried and was gonna try after the call.

    Only follow the above crieterias. Just return the rating in 0 or 2, without any other text.
    """

    prompt3 = """"Based on the following transcript between the agent and the customer you have to evaluate only Agent's dialogue's performance, considering clarity and politeness. Provide a single overall score between 0 and 2, where 0 is poor, 1 is neutral, and 2 is good
    Only follow the above crieterias. Just return the rating between 0 to 2, without any other text.

    """

    system_prompt_2 = """Based on the following transcript between the agent and the customer you have to evaluate only Agent's dialogue's performance, considering clarity and politeness. Provide a single overall score between 0 and 2, where 0 is poor, 1 is neutral, and 2 is good. Justify your rating with specific examples from the transcript. You can use the following criteria
    
    Examples of 0 
    - The agent guided customer through reinstalling the application despite communication gaps and some impatience. The call concluded with instructions to reinstall, though the resolution's effectiveness remains unclear. -> 0

    - The call was from a customer regarding account closure issues. Despite frustration over delays in receiving closure instructions, the agent handled the call assertively, securing agreement for closure within seven days despite tensions. -> 0

    - The call was from a customer inquiring about account opening charges. The agent addressed the customer's concerns about unexpected charges and suggested contacting the relationship manager for resolution. Despite frustrations, the agent remained patient and offered to adjust brokerage charges, demonstrating professionalism throughout the call. -> 0

    - The call was from customer to the company agent. He had an issue with his application not opening. The agent guided Abhishek through reinstalling the application despite communication gaps and some impatience. The call concluded with instructions to reinstall, though the resolution's effectiveness remains unclear. -> 0

    
    Examples of 2:
    - The call was from a customer who was having trouble with their password. The customer was trying to figure out how to view their password on another phone. The agent guided the customer to click on 'Forgot Password' and create a new password. The customer seemed to be having difficulty following the instructions and was not able to see the password on the other phone. The agent patiently continued to assist the customer by suggesting to change the password by clicking on 'Forgot Password' and then logging in with the client ID. The customer was still confused and asked the agent to tell them the password, but the agent explained that the password is personal and needs to be created by the customer. The agent tried to guide the customer on how to change the password by clicking on 'Forgot Password' and following the steps to create a new password. The customer eventually agreed to try creating a new password on their own. The agent remained patient and provided step-by-step instructions to help the customer resolve the issue. Overall, the call was smooth with the agent being polite and understanding towards the customer's confusion regarding the password. -> 2

    - The call was from the customer to the company agent regarding their account opening. The customer seemed to be frustrated and kept repeating numbers during the call. The agent tried to assist the customer by asking for coordinates and guiding them through the process. The agent was polite and patient throughout the call, despite the customer's repeated numbers and frustration. The call seemed to have a few problems with the customer's communication, but the agent handled it with empathy and tried to help the customer to the best of her ability. Overall, the agent handled the call professionally and tried to assist the customer in resolving their query.

    - The call was from a customer regarding a modification done through courier services. The customer was unsure about the pen number related to the Indore branch. The agent informed the customer to contact the customer care for details regarding the franchise. The customer confirmed being associated with the French franchise. The agent provided the customer with the customer care number and asked them to call for further assistance. The call ended with the agent thanking the customer. The agent was not rude or disrespectful towards the customer, but there was a slight miscommunication regarding the customer care number. Overall, the call was smooth with no major issues.

    Only follow the above crieterias. Just return the rating between 0 to 2, without any other text
    """

    user_prompt = f"Transcript:{transcript}\n Summary: {summary}, check how empathetic the agent was towards the client. And only return a rating between 0 and 2 without any extra text."


    completion = client.chat.completions.create(
        temperature=0,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": new_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return int(completion.choices[0].message.content)

def check_closure(transcript: str, summary: str) -> int:
    """
    Description: This function checks if the agent gave a proper closure to the client during the call. 

    parameters: 
        - tranascript (str): Call transcript

    returns: 
        - closure_score (int): Returns 0 if the agent did not give a proper closure, and returns 1 if he gave a closure.         
    """

    system_prompt = """You are a professional HINDI sales call analyzer. Your job is to make sure that the agent concluded the call well by either saying thankyou, asking the customer if there's anything he needs help with, give follow up instructions etc. 
    Eg:  Can I assist you with anything else? Thank you sir have a nice day? Is there anything you need help with? etc. 
    You will be given a hindi transcript and have to return 1 if the agent did the closure well and return 0 if the agent did not say anything in the closure. basically any closure asking clients/customers if they need anything else in hindi.Only reply in 1 and 0 nothing else."""

    user_prompt = f"For the given transcript{transcript}\n For the given summary: {summary}. Reply 1 if the agent concluded the call well and 0 if the agent did not conclude the call well"

    completion = client.chat.completions.create(
        temperature=0,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return int(completion.choices[0].message.content)

def generate_sumary(transcript: str, agentName: str) -> str:
    """
    Description: This function generates summary for a given transcript. 
    parameters: 
        - transcript (str): Call transcript
    returns:
        - summary (str): Summary generated by open AI
    """

    system_prompt = f"""Create a summary of a call recording between a customer and the agent. The call will always be an incoming call from the customer to the agent named {agentName}.
    Include the following points: 
    1 Mention if the agent exchanged any greetings or plesentaries with the customer and what did he say.
    2. who called whom, 
    3. Was the agent was being mean and seemed uninterested to solve the queries of the customer. Was the agent interrupting the customer and raising his voice desipte using polite words, Did the agent get impatient despite the customer talking properly.
    4. If the agent got frustrated, did the agent handle the conversation with care, politeness and empathy or did he get frustrated too. 
    5. problem description by the customer
    6. steps taken by the agent to assist
    7. resolution or outcome of the issue
    8. any commitments made for follow-up
    9. Did the agent answer all questions by the client. Was the client satisfied with the solution. 
    10. Did the agent talk in a different language than the customer,  
    11. Mention if the agent concluded the call well. Eg (Thanked the customer or confirmed next steps, etc., ensured of follow-up, etc. )
    
    return summary in a paragraph format and not bullet points."""
    user_prompt = f"{transcript}, for the given transcript generate a summary. "

    completion = client.chat.completions.create(
        temperature=0,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return completion.choices[0].message.content