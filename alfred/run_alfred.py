from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from nlp_processor import NLProcessor
from generate_response import get_reply
from helpers import *
from phue import Bridge
import pyowm
from bin.testingAlfred import testing

app = Flask(__name__)

################################### SETUP ###################################
# any steps to take when the script is first run are here
print('[INFO] Setting up...')
# parse and store command line arguments
arguments = parse_args()
# parse and store config file
config = configurations(arguments.config)
# initilize our NLProcessor object
print('[INFO] Initilizing NL Processor...')
processer = NLProcessor()

## PHILIPS HUE
hue_config = config['lights']
if hue_config['bridgeIP'] != 'None':
    # create the Bridge object with correct IP
    print('[INFO] Connecting to Philips Hue Bridge with IP {}...'.format(hue_config['bridgeIP']))
    philips_bridge = Bridge(hue_config['bridgeIP'])
    # warn user about connect process with hub
    if arguments.connectBridge:
        print('''[INFO] Make sure you have pressed the button on the Hue Bridge
        within 30 seconds of running this script...\n''')
        philips_bridge.connect()
else:
    philips_bridge = None
## WEATHER
weather_config = config['weather']
if weather_config['OWMKey'] != 'None':
    print('[INFO] Setting up pyowm with API key {}...'.format(weather_config['OWMKey']))
    owm = pyowm.OWM(weather_config['OWMKey'])
else:
    owm = None

## TESTING
# if test flag is passed, run a test loop
if arguments.test:
    testing(processer, philips_bridge, owm)

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
    app.run(debug=True)
