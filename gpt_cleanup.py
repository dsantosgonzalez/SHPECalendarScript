import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Can you find any relevant events in this text and format them in this format Name: [name of "
                       "event]\nDescription: [description of event]\nStart: [start date and time]\n",
        }
    ],
    model="gpt-3.5-turbo",
)
