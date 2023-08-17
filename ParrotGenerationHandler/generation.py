from twilio.rest import Client

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import string
import os
import openai
import json


def generation_handler(event, context):
    openai.api_key = os.environ.get("OPENAI_KEY")

    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_auth = os.environ.get("TWILIO_AUTH")
    twilio_client = Client(twilio_sid, twilio_auth)

    MY_PHONE = os.environ.get("PHONE_NUM")
    TWILIO_NUMBER = os.environ.get("TWILIO_NUM")

    FIRST_ELEMENT = 0

    prompt = "Generate a simple random topic or event in 7 words or less"
    query = [{"role": "user", "content": prompt}]
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=query
    )

    reply = chat.choices[FIRST_ELEMENT].message.content
    quote_prompt = "Generate a single sentence, simple quote with about {} in 10 words or less".format(reply)
    quote_query = [{"role": "user", "content": quote_prompt}]

    quote_chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=quote_query
    )

    end_quote = quote_chat.choices[FIRST_ELEMENT].message.content.translate(str.maketrans('', '', string.punctuation))

    sting_prompt = "Generate 2 words relating to {} with no punctuation".format(reply)
    sting_query = [{"role": "user", "content": sting_prompt}]

    sting_chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=sting_query
    )

    sting_result = sting_chat.choices[FIRST_ELEMENT].message.content.lower().translate(str.maketrans('', '', string.punctuation))

    linkedin = "Wow! {} - {}!".format(end_quote, sting_result)
    print(linkedin)

    message = twilio_client.messages.create(
        to=MY_PHONE,
        from_=TWILIO_NUMBER,
        body="Quote: ${}@\nIs this post good? (Y or N)".format(linkedin))

    body = {
        "message": "Generated quote!"
    }
    return {"statusCode": 200, "body": json.dumps(body)}
