import re

from nltk import tokenize

import wikipedia
from phue import Group

from .process_input import *

# from webcolors import name_to_hex

# (TODO) Figure out a better way to connect with Bridge each time

def weatherAction(message, nlp, owm):
    """Makes the appropriate calls to the OWM API to answer weather queries.

    Args:
        message (str): An incoming text message.
        nlp: Instance of NLProcessor class
        owm: Instance of OWM API object

    Returns:
        A message answering the weather query.
    """
    # create the spacy doc object
    doc = nlp(message)
    # get all GPE (geopolitical entity) mentions
    location_mentions = [ent.text for ent in doc.ents if ent.label_ == 'GPE']

    # attempt to join city/state/country mentions.
    location = ', '.join(location_mentions)
    try:
        # this object contains all the methods to get to the data
        observation = owm.weather_at_place(location)
        # get the weather and locations objects
        w, l = observation.get_weather(), observation.get_location()
        # get location name (according to owm)
        city = l.get_name()

        # extract the data to return
        wind_speed = str(w.get_wind()['speed'])
        temp = str(w.get_temperature('celsius')['temp'])
        status = str(w.get_detailed_status())
        answer = '''{} in {}, with a temperature of {}C and winds {}km/h.'''.format(status.title(), city, temp, wind_speed)
    except:
        # handle all errors with one error message
        answer = "Request cannot be completed. Try 'weather Toronto, Canada (proper capitlization of locations helps me identify them!)'"

    return answer

def lightsAction(message, philips_bridge):
    """Makes the appropriate calls to the phue API for changing light settings based on message and
    generates a response.

    Args:
        message (str): An incoming text message.
        apis['philips_bridge']: Instance of phue API bridge object

    Returns:
        A message indicating what action was taking with the phue API.
    """
    # set default answer to error message
    answer = "Something went wrong..."
    # by default, set lights to all lights
    lights = philips_bridge.lights
    # get the names of all lights
    light_names = [l.name.lower() for l in lights]
    # get the name of all rooms (Hue calls these 'groups')
    groups = philips_bridge.get_group()
    room_names = [groups[key]['name'] for key in groups]

    # look for room-specific mentions in the sms. If room name mentioned
    # set lights equal to all lights in this group
    mentioned_room = ''
    for room in room_names:
        if re.search(room.lower(), message):
            mentioned_room = room.lower() + ' '
            lights = Group(philips_bridge, room).lights

    # use regex and cascading rules to determine action to take with lights
    # 1) Setting lights to a certain % intensity
    if re.search(r"%|\bpercent\b|\bdim\b", message):
        """
        Example text:
            - 'dim bedroom lights'
            - 'set lights to 50%'
        """
        # if the word is dim is mentioned, set to 15%
        if re.search('dim', message):
            intensity = '15'
        # else find the value that directly proceeds '%' or 'percent'
        else:
            intensity = re.findall(r'(\w+)\s*(%|percent)\s*', message)[0][0]
        try:
            for l in lights:
                l.on = True
                # normalize % intensity to a value between 0-254
                l.brightness = int(int(intensity)/100*254)
                answer = "Setting {}lights to {}%...\U0001F4A1".format(mentioned_room, intensity)
        except:
            answer = 'Something went wrong while trying to change your lights brightness...'

    # 2) Turning lights off
    elif re.search(r"\boff\b", message):
        """
        Example text:
            - 'turn off the bedroom lights'
            - 'turn off the lights'
        """
        try:
            for l in lights:
                l.on = False
            answer = "Turning {}lights off...\U0001F4A1".format(mentioned_room)
        except:
            answer = 'Something went wrong while trying to turn your lights off...'
    # 3) Turning lights on
    elif re.search(r"\bon\b", message):
        """
        Example text:
            - 'turn on the bedroom lights'
            - 'turn on the lights'
        """
        try:
            for l in lights:
                l.on = True
                l.brightness = 254
            answer = "Turning {}lights on...\U0001F4A1".format(mentioned_room)

        except:
            answer = 'Something went wrong while trying to turn your lights on...'
    # 4) Warming or cooling lights
    elif re.search(r"\bwarm\b|\bcool\b", message, re.IGNORECASE):
        """
        Example text:
            - 'Warm the bedroom lights'
            - 'Cool the lights'
        """
        warmOrCool = ''
        # check if warm or cool was mentioned
        if re.search(r'warm', message, re.IGNORECASE):
            warmOrCool = 'Warming'
        elif re.search(r'cool', message, re.IGNORECASE):
            warmOrCool = 'Cooling'
        # turn on and then warm or cool lights accordingly
        try:
            for l in lights:
                l.on = True
                # cool or warm lights
                if warmOrCool == 'Warming':
                    l.colortemp_k = 2000
                    # additionaly set lights to 60% brightness
                    l.brightness = 152
                elif warmOrCool == 'Cooling':
                    l.colortemp_k = 6500
                    # additionaly set lights to 80% brightness
                    l.brightness = 254
            answer = "{} {}lights...\U0001F4A1".format(warmOrCool, mentioned_room)
        except Exception as exception:
            answer = 'Something went wrong while trying to warm or cool your lights...'
    # 5) Change the lights color
    # NOTE THIS IS A BIT OF A HACK, NEEDS TO BE IMPROVED
    else:
        """
        Example text:
            - 'Turn the lights blue'
            - 'Turn the bedroom lights red'
        """
        # tokenize
        tokens = tokenize.wordpunct_tokenize(message)
        # filter stopwords
        tokens_filtered = remove_stopwords(tokens)
        # join filtered message
        message_filtered = ' '.join(tokens_filtered)
        print("(Highly) processed input: ", message_filtered)
        # find the mention of a color name
        color = re.findall(r'\s*lights?\s*(\w+)', message_filtered)[0]
        # THIS IS A TEMPORARY HACK
        colors = {
            'blue': 40000,
            'red': 100,
            'green': 30000,
            'orange': 4000,
            'pink': 60000,
            'purple': 50000,
        }
        try:
            for l in lights:
                l.on = True
                l.brightness = 254
                # this is necessary to reproduce colours accurately
                l.colortemp_k = 2000
                l.hue = colors[color]
            answer = "Turning {}lights {}...\U0001F4A1".format(mentioned_room, color)
        except:
            answer = 'Something went wrong while trying to change the color of yours lights...'
    # return final answer
    return answer

def wikipediaAction(message):
    """Makes the appropriate calls to the wikipedia API for answer wiki queries.

    Args:
        message (str): An incoming text message.

    Returns:
        A message indicating what action was taking with the wikipedia API.
    """
    message = sterilize(message)
    # tokenize input
    tokens = tokenize.wordpunct_tokenize(message)
    # filter stopwords, additionally, remove 'wiki' or 'wikipedia'
    tokens_filtered = remove_stopwords(tokens)
    tokens_filtered = [token for token in tokens_filtered
                       if token.lower() != 'wiki' and token.lower() != 'wikipedia']
    # join filtered message
    message = ' '.join(tokens_filtered)

    # for debugging/testing
    print("(Highly) processed input: ", message)

    # Get the wikipedia summary for the request
    try:
        summary = wikipedia.summary(message, sentences = 1)
        url = wikipedia.page(message).url
        answer = summary + "\nSee more here: " + url
        if len(answer) > 500:
            answer = answer[0:500] + "\nSee wikipedia for more..."
    except:
        # handle all errors
        answer = "Request was not found using Wikipedia. Be more specific?"

    return answer

def wolframAction():
    pass

def get_reply(message, nlp, apis):
    """
    This method processes an incoming SMS and makes calls to the appropriate
    APIs via other methods.

    Args:
        message (str): An incoming text message.
        apis (dict): A dictionary containing any API objects we need to generate replies.
        nlp: Instance of Spacy NLP object.

    Returns:
        A response to message either answering a request or indicating what actions were taken.
    """
    ## TEXT PREPROCESSING
    message = sterilize(message)
    print("(Simply) processed input: ", message)

    # Look for keyword triggers in the incoming SMS
    ## WEATHER
    if re.search(r'\b(?i)weather\b', message):
        if apis['owm'] != None:
            print('here')
            answer = weatherAction(message, nlp, apis['owm'])
        else:
            answer = "Hmm. It looks like I haven't been setup to answer weather requests. Take a look at the config.ini file!"
    ## WOLFRAM
    elif re.search("(?i)wolfram", message,):
        if apis['wolfram'] != None:
            answer = wolframAction(message)
        else:
            answer = "Hmm. It looks like I haven't been setup to answer Wolfram requests. Take a look at the config.ini file!"
    ## WIKI
    elif re.search(r'(?i)wiki(pedia)?', message):
        answer = wikipediaAction(message)
    # LIGHTS
    elif re.search(r'(?i)lamps?|(?i)lights?', message):
        if apis['philips_bridge'] != None:
            answer = lightsAction(message, apis['philips_bridge'])
        else:
            answer = "Hmm. It looks like I haven't been setup to work with your Hue lights. Take a look at the config.ini file!"
    # the message contains no keywords. Display help prompt
    else:
        answer = ("\nStuck? Here are some things you can ask me:\n\n'wolfram' "
                  "{a question}\n'wiki' {wikipedia request}\n'weather' {place}\n'turn lights off'\n"
                  "\nNote: some of these features require additional setup.")
    # return the formulated answer
    return answer
