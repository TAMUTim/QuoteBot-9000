# Alright this is just to test out some of the functionality of GPT / TWILIO
# First check out OpenAI / ChatGPT

from dotenv import load_dotenv
from twilio.rest import Client
import os
import openai

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"

prompt = "Generate a simple random topic or event in 7 words or less"

query = [{"role": "user", "content": prompt}]

chat = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=query
)

reply = chat.choices[0].message.content

quote_prompt = "Generate a single sentence, simple quote about {} in 10 words or less".format(reply)

quote_query = [{"role": "user", "content": quote_prompt}]

quote_chat = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=quote_query
)

end_quote = quote_chat.choices[0].message.content

print("TOPIC:", reply)
print("END RESULT:", end_quote)

twilio_sid = os.environ.get("TWILIO_SID")
twilio_auth = os.environ.get("TWILIO_AUTH")
twilio_client = Client(twilio_sid, twilio_auth)

linkedin = "Wow! {}".format(end_quote[1:-1])

message = twilio_client.messages.create(
    to="+18329517889",
    from_="+18449693712",
    body="Quote: {}\nIs this good?".format(linkedin))

print(message.sid)
