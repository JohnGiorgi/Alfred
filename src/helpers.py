import configparser
import argparse
import sys
import os
from phue import Bridge
import time
from phue import Bridge
import pyowm
import sys
from bin.testingAlfred import testing

def initial_setup():
    """Initial setup to be called when Alfred Flask app is run"""

    # (TODO) Should not respond to numbers it does not recognize
    # (TODO) Complete action for one light when light name is mentioned
    # (TODO) Testing script should be unique

    # add <number>:<name> key pair values to have Alfred respond using your name
    callers = {
    }

    print('[INFO] Setting up...')

    # parse and store command line arguments
    arguments = parse_args()

    ## SETUP
    # if setup flag is passed, run guided setup loop
    if arguments.setup:
        guided_setup()
        # terminate script after setup
        sys.exit

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
            philips_bridge = Bridge()
            print("""
            [INFO] Make sure you have pressed the button on the Hue Bridge within 30
            seconds of running this script...\n
            [INFO] Your bridge ip is {}
            """.format(philips_bridge.get_ip_address()))
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
        testing(philips_bridge, owm)
def configurations(path):
    """Parses and reads the configuration file named found at path. Returns
    a configparser Object."""
    # create config parsing object
    config = configparser.ConfigParser()
    # read config
    config.read(path)
    return config
def parse_args():
    """
    This method creates an ArgumentParser object, creates and defines all
    arguments to be used by run_sms_bot.py, and returns all captured
    arguments as an argparse object"""

    ## create parser
    parser = argparse.ArgumentParser(description='''Run Alfred, a simple
    Flask app which recieves messages sent to a Twilio number and returns
    a response back to the sender. This app interacts with other APIs
    such as the Philips Hues API, WolframAlpha API, and OWM API in order
    to carry out actions.''')

    ## add arguments
    # --config
    parser.add_argument('--config', metavar = '<configuration file>',
    type = str, help = '''Enter the path to the configuration file. Default is
    at src/config.ini''', default = 'config.ini')
    # --connectBridge
    parser.add_argument('--connectBridge', action = 'store_true', help = '''If
    you intend to use the script with you Hue Bridge, set this to True when you
    run the script for the first time''', default = False)
    # --test
    parser.add_argument('--test', action = 'store_true', help = '''Pass this flag
    in order to run a testing loop which allows you to enter text to Alfred from the
    command line''', default = False)
    # --setup
    parser.add_argument('--setup', action = 'store_true', help = '''Pass this flag
    in order to run a guided setup with Alfred''', default = False)

    try:
        arguments = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    return arguments
def guided_setup():
    # (TODO): Need to update the config file with the bridgeIP
    # (TODO): Need to fix formatting
    # (TODO): Blinking is not working as expected

    # intial prompt
    print("Hi, I'm Alfred, lets get setup. Press ENTER to continue...")
    input()
    # prompt user about Phillips Hue
    huePrompt = input("Would you like me to be able to control your Phillips Hue lights (y/n)?: ").lower()
    time.sleep(0.8)
    # run while loop if user enters incorrect answer
    while huePrompt != 'y' and huePrompt != 'n':
        print("Sorry, I didn't understand your answer...")
        huePrompt = input("Would you like me to be able to control your Phillips Hue lights (y/n)?: ")
        time.sleep(0.8)
    # if user answered yes, connect to bridge
    if huePrompt == 'y':
        # display useful tips
        print("Note: Please make sure your Phillips Hue bridge is on the same network as I am running on!")
        time.sleep(0.8)
        # prompt for bridge IP
        bridgeIPPrompt = input("Please enter the IP of your Phillips Hue bridge (instructions for locating this can be found here: https://developers.meethue.com/documentation/getting-started): ").strip()
        time.sleep(0.8)
        print("Great, I will connect to the Bridge with IP {} (if it exists!)".format(bridgeIPPrompt))
        # create bridge object
        b = Bridge(bridgeIPPrompt)
        print("Please press the button on your Phillis Hue bridge, then within 30 seconds and press ENTER here...")
        input()
        # connect to bridge object
        b.connect()
        # blink lights
        print("I am going to turn off all your lights, and then turn them back on to make sure things are working properly. Ready? Press ENTER to continue.")
        input()
        lights = b.lights
        for l in lights:
            # turn lights off if they are on and on if they are off
            for i in range(3):
                l.on = not l.on
            time.sleep(1)
        # check that blink worked, if not display helpful tips
        blinkPrompt = input("Did your lights blink (y/n)?: ").lower()
        time.sleep(0.8)
        while blinkPrompt != 'y' and huePrompt != 'n':
            print("Sorry, I didn't understand your answer...")
            blinkPrompt = input("Did your lights blink (y/n)?: ").lower()
            time.sleep(0.8)
        if blinkPrompt == 'y':
            print('Great! I will end our setup. You can now run: python src/run_alfred.py')
        else:
            print('''Try running this script again. Ensure that\n
            - The bridge is on the same network as the computer I am running on\n
            - You pressed the button on the bridge when I instructed you to\n
            - You provided me with the correct IP address for the bridge''')
