import os
from openai import OpenAI, openai


client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY", ""),
)

def generatePrompt(prompt):

    response = openai.ChatCompletion.create(
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