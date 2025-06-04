import os
from openai import OpenAI


client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY", ""),
)

def sendDummyRequest():
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

def generatePrompt(prompt):

    response = client.ChatCompletion.create(
        model="models/gpt-3.5-turbo",
        messages=[
            {
                "role": "user", 
                "content": "Generate a detailed SEO report for the following keyword: " + prompt
            }
            ],
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()