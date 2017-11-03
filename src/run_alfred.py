# (TODO): Fix recognition of caller issue.

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from generate_response import get_reply
from helpers import *

app = Flask(__name__)

### THE BOT
@app.route("/", methods=['GET', 'POST'])
def smsbot():
    """This method recieves the text and controls the response.

    Returns:
        Alfreds response to the incoming message (str)
    """
    # get the phone number, city and country request was sent from

    # from_number = request.values.get('From', None)
    # from_city = request.values.get('FromCity', None)
    # from_country = request.values.get('FromCountry', None)

    # prepend custom message if number is recognized

    # if from_number in callers:
    #    message = "Ok " + callers[from_number] + "\U0001f604\n\n"

    # get the body of the incoming sms
    message_body = request.form['Body']
    # send this to get_reply which calls appropriate API's
    alfreds_response = get_reply(message_body, philips_bridge, owm, wolfram)

    return str(MessagingResponse().message(alfreds_response))

if __name__ == "__main__":
    # parse parameters and config file
    philips_bridge, owm, wolfram = initial_setup()
    # run flask app
    app.run(debug=True)
