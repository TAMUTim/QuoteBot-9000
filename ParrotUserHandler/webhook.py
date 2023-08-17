from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

import boto3
import os
import json
import time
import datetime

client = boto3.client("lambda")

app = Flask(__name__)

@app.route('/', methods=['POST'])
def incoming_message():
    resp = MessagingResponse()

    twilio_client = Client(os.environ.get("TWILIO_SID"), os.environ.get("TWILIO_AUTH"))
    TWILIO_NUMBER = os.environ.get("TWILIO_NUM")
    MY_PHONE = os.environ.get("PHONE_NUM")
    
    FIRST_ELEMENT = 0

    received_history = twilio_client.messages.list(to=TWILIO_NUMBER, from_=MY_PHONE)
    sent_history = twilio_client.messages.list(to=MY_PHONE, from_=TWILIO_NUMBER)

    current_time = datetime.datetime.utcnow()

    latest_message_from_tim = received_history[FIRST_ELEMENT]
    latest_message_from_twilio = sent_history[FIRST_ELEMENT]
    tim_time_sent = latest_message_from_tim.date_sent
    twilio_time_sent = latest_message_from_twilio.date_sent


    if twilio_time_sent.date() != current_time.date():
        resp.message("Sorry, no quote has been generated today, try later.")
        return str(resp), 200, {'Content-Type': 'application/xml'}

    if twilio_time_sent <= tim_time_sent:
        if latest_message_from_tim.body.lower() == "y" or latest_message_from_tim.body.lower() == "yes":
            # invoke the post guy here
            print("Response accepted, posting to linkedIn")
            quote = ''.join(latest_message_from_twilio.body.split('$')[1].split('@')[0])
            client.invoke(
                FunctionName='',
                InvocationType='RequestResponse',
                Payload=json.dumps({"content": quote})
            )
        else:
            # invoke the regeneration process here
            print("Quote not good, exiting verification process")
        
    return {"statusCode": 200}
