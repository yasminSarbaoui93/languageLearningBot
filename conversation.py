# All API requests should include your API key in an Authorization HTTP header as follows: Authorization: Bearer OPENAI_API_KEY
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def callOpenAI(user_message)
    try:
        response = openai.completions.create(
            model="gpt-4o"
            messages=[{"role": "user", "content": user_message}]
            temperature=0.7
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"
    



from openai import OpenAI

client = OpenAI()

def LLMcall(message, bot, german_words)
    #define the function that will call openai
    #call the openai API
    #get the response from the API
    #send the response to the user
    #ask the user to translate the word
    #check the user response

stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")