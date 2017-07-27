import configparser
import argparse
import sys

def configurations(path):
    """Parses and reads the configuration file named found at path. Returns
    a configparser Object"""
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

    try:
        arguments = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    return arguments
