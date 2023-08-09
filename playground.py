# Alright this is just to test out some of the functionality of GPT / TWILIO
# First check out OpenAI / ChatGPT

from dotenv import load_dotenv
import os
import openai
import requests

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"

prompt = "Hi there, please tell me a joke"

query = [{"role": "user", "content": prompt}]

chat = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=query
)

print(chat)
