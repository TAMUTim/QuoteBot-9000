# Alright this is just to test out some of the functionality of GPT / TWILIO
# First check out OpenAI / ChatGPT

from dotenv import load_dotenv
from twilio.rest import Client
from email import utils
import datetime
import os
import openai
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

linkedin_user = os.environ.get("LINKEDIN_USER")
linkedin_pass = os.environ.get("LINKEDIN_PASS")

twilio_sid = os.environ.get("TWILIO_SID")
twilio_auth = os.environ.get("TWILIO_AUTH")
twilio_client = Client(twilio_sid, twilio_auth)

MY_PHONE = "+18329517889"
TWILIO_NUMBER = "+18449693712"

TWILIO_RETRY_TIME = 5
FIRST_ELEMENT = 0

OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"
LINKEDIN_SITE = 'https://www.linkedin.com'


def post_to_linkedin(contents):
    driver = webdriver.Chrome()
    driver.get(LINKEDIN_SITE)
    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="session_key"]').send_keys(linkedin_user)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="session_password"]').send_keys(linkedin_pass)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'sign-in-form__submit-btn--full-width').click()
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'share-box-feed-entry__trigger').click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'ql-editor.ql-blank').send_keys(contents)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, 'share-actions__primary-action').click()
    time.sleep(20)


def verify_response():
    received_history = twilio_client.messages.list(to=TWILIO_NUMBER, from_=MY_PHONE)
    sent_history = twilio_client.messages.list(to=MY_PHONE, from_=TWILIO_NUMBER)

    if not received_history:
        time.sleep(TWILIO_RETRY_TIME)
        return verify_response()

    latest_message_from_tim = received_history[FIRST_ELEMENT]
    latest_message_from_twilio = sent_history[FIRST_ELEMENT]
    tim_time_sent = latest_message_from_tim.date_sent
    twilio_time_sent = latest_message_from_twilio.date_sent

    if twilio_time_sent <= tim_time_sent:
        if latest_message_from_tim.body.lower() == "y" or latest_message_from_tim.body.lower() == "yes":
            return True
        else:
            return False
    else:
        time.sleep(TWILIO_RETRY_TIME)
        return verify_response()


def get_valid_quote():
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

    linkedin = "Wow! {}".format(end_quote[1:-1])

    message = twilio_client.messages.create(
        to=MY_PHONE,
        from_=TWILIO_NUMBER,
        body="Quote: {}\nIs this good?".format(linkedin))

    valid = verify_response()

    if valid:
        return linkedin
    else:
        return get_valid_quote()


def main():
    # post_to_linkedin(get_valid_quote())
    # want to try out selenium'
    quote = get_valid_quote()
    print("posting to linkedin now this: {}".format(quote))
    # post_to_linkedin("go big mode!")


if __name__ == "__main__":
    main()
