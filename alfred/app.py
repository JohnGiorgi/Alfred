import argparse

from flask import Flask, request

from twilio.twiml.messaging_response import MessagingResponse

from . import response
from .utils.utils import initial_setup, load_spacy_model

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def alfred():
    """This method recieves the SMS message and controls the response.

    Returns:
        Alfreds response to the incoming message as a string.
    """
    # get the body of the incoming sms
    message_text = request.form['Body']
    # message_number = request.values.get('From', None)

    # send this to get_reply which calls appropriate API's
    alfreds_response = response.get_reply(message_text, nlp, apis)

    resp = MessagingResponse()
    resp.message(alfreds_response)

    return str(resp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Run Alfred, a simple Flask app which recieves
    messages sent to a Twilio number and returns a response back to the sender. This app interacts
    with other APIs such as the Philips Hues API, WolframAlpha API, and OWM API in order to carry
    out actions.''')
    # --config
    parser.add_argument('--config', type=str, default='alfred/config.ini',
    help='Enter the path to the configuration file. Default is at src/config.ini')
    # --setup
    parser.add_argument('--setup', action='store_true', default=False,
    help='Pass this flag in order to run a guided setup with Alfred')

    args = parser.parse_args()

    philips_bridge, owm, wolfram = initial_setup(args.config, args.setup)
    apis  = {'philips_bridge': philips_bridge, 'owm': owm, 'wolfram': wolfram,}

    # SpaCy NLP object for all text processing and NLP tasks
    nlp = load_spacy_model()

    app.run(debug=False)
