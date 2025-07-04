from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY)

completion = client.chat.completions.create(
  model="gpt-4.1-mini",
    messages=[
      {
        "role": "user",
        "content": "What is the capital of France?"
      }
  ]
)

print(completion.choices[0].message.content)