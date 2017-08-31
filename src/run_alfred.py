from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from generate_response import get_reply
from helpers import *

app = Flask(__name__)

### THE BOT
@app.route("/", methods=['GET', 'POST'])
def smsbot():
    """This method recieves the text and controls the response"""
    # create empy message string by default
    message = ""
    # get the phone number, city and country request was sent from
    from_number = request.values.get('From', None)
    from_city = request.values.get('FromCity', None)
    from_country = request.values.get('FromCountry', None)
    from_location = from_city + ", " + from_country
    # prepend custom message if number is recognized
    if from_number in callers:
        message = "Ok " + callers[from_number] + "\U0001f604\n\n"
    # get the body of the incoming sms
    message_body = request.form['Body']
    # send this to get_reply which calls appropriate API's
    message = message + get_reply(message_body, processer, philips_bridge, owm)
    # create MessageResponse() object and add our response to it
    resp = MessagingResponse().message(message)
    # return the reponse to the user
    return str(resp)

if __name__ == "__main__":
    # parse parameters and config file
    initial_setup()
    # run flask app
    app.run(debug=True)
