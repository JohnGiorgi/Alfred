import re
import wikipedia

# (TODO) Figure out a better way to connect with Bridge each time
# (TODO) Use location of user somehow! https://www.twilio.com/docs/api/twiml/sms/twilio_request

def lightsAction(message, processer, philips_bridge):
    """
    Makes the appropriate calls to the phue API for changing light settings
    based on message and generates a response.

    Args:
        message: An incoming text message
        philips_bridge: Instance of phue API bridge object

    Returns:
        A message indicating what action was taking with the phue API
    """
    answer = "Something went wrong..."
    # use regex and cascading grammer
    # by default, set lights to all lights
    lights = philips_bridge.lights
    # get the names of all lights
    light_names = [l.name.lower() for l in lights]

    # look for room specific mentions in the sms. if mentioned name
    # exists on the bridge, set lights equal to light objects with this name
    rooms = []
    for x in light_names:
        if re.search(x, message):
            rooms.append(x)
    if len(rooms) != 0:
        lights = [l for l in lights if l.name.lower() in rooms]

    # determine what action to take with the lights
    # 1) Setting lights to a certain % intensity
    if re.search("%|percent|dim", message):
        # if the word is dim is mentioned, set to 15%
        if (re.search('dim', message)):
            intensity = '15'
        else:
            intensity = re.findall('(\w+)\s*(%|percent)\s*', message)[0][0]
        try:
            for l in lights:
                l.on = True
                # normalize % intensity to a value between 0-254
                l.brightness = int(int(intensity)/100*254)
                answer = "Setting {} lights to {}%...\U0001F4A1".format(', '.join(rooms), intensity)
        except:
            answer = 'Something went wrong while trying to change your lights brightness...'

    # 2) Turning lights off
    elif re.search("off", message):
        try:
            for l in lights:
                l.on = False
            answer = "Turning {} lights off...\U0001F4A1".format(', '.join(rooms))
        except:
            answer = 'Something went wrong while trying to turn your lights off...'
    # 3) Turning lights on
    elif re.search("on", message):
        try:
            for l in lights:
                l.on = True
                l.brightness = 254
            answer = "Turning {} lights on...\U0001F4A1".format(', '.join(rooms))

        except:
            answer = 'Something went wrong while trying to turn your lights on...'
    '''
    # 4) Change the lights color
    else:
        # tokenize
        tokens = processer.tokenize(message)
        # filter stopwords
        tokens_filtered = processer.stopwordFilter(tokens, 'resources/data/stopwords.txt')
        # join filtered message
        message_filtered = ' '.join(tokens_filtered)
        print("(Highly) processed input: ", message_filtered)
        # find the mention of a color name
        color = re.findall('\s*lights?\s*(\w+)', message_filtered)[0]
        # convert this to a hex code
        name_to_hex(color)
    '''


    return answer
def weatherAction(message, processer, pyowm_object):
    """
    Makes the appropriate calls to the OWM API for answer weather queries

    Args:
        message: An incoming text message
        processer: Instance of NLProcessor class
        pyowm_object: Instance of OWM API object

    Returns:
        A message answering the weather query
    """
    answer = ""
    # tokenize input
    tokens = processer.tokenize(message)
    # filter stopwords
    tokens_filtered = processer.stopwordFilter(tokens, 'resources/data/stopwords.txt')
    # join filtered message
    message_filtered = ' '.join(tokens_filtered)
    print("(Highly) processed input: ", message_filtered)
    # find the word that occurs after weather, looking for a city
    location = re.findall('\s*weather\s*(\w+)', message_filtered)[0]
    try:
        # this object contains all the methods to get to the data
        observation = pyowm_object.weather_at_place(location)
        # get the weather object
        w = observation.get_weather()
        # get the location object
        l = observation.get_location()
        # store the data to return
        city = l.get_name()
        wind_speed = str(w.get_wind()['speed'])
        temp = str(w.get_temperature('celsius')['temp'])
        status = str(w.get_detailed_status())

        answer = "{} in {}, with a temperature of {}C and winds {}km/h.".format(status, city, temp, wind_speed)

    except:
        # handle errors or non specificity errors
        answer = "Request cannot be completed. Try 'weather Toronto, Canada'"


    return answer
def wikipediaAction(message, processer):
    answer = "Something went wrong..."
    # tokenize input
    tokens = processer.tokenize(message)
    # filter stopwords
    tokens_filtered = processer.stopwordFilter(tokens, 'resources/data/stopwords.txt')
    # join filtered message
    message = ' '.join(tokens_filtered)
    # remove the keyword "wiki(pedia)?" from the message
    message = message.replace("wikipedia", "")
    message = message.replace("wiki", "")
    print("(Highly) processed input: ", message)
    # Get the wikipedia summary for the request
    try:
        summary = wikipedia.summary(message, sentences = 1)
        url = wikipedia.page(message).url
        answer = summary + "\nSee more here: " + url
        if len(answer) > 500:
            answer = answer[0:500] + "\nSee wikipedia for more..."
    except:
        # handle errors or non specificity errors (ex: there are many people named donald)
        answer = "Request was not found using Wikipedia. Be more specific?"

    return answer

def get_reply(message, processer, philips_bridge, pyowm_object):
    """
    This method processes an incoming SMS and makes calls to the appropriate
    APIs via other methods.

    Args:
        message: An incoming text message
        location: Location the request was sent from based on phone number
        processer: Instance of NLProcessor class
        philips_bridge: Instance of phue API bridge object
        pyowm_object: Instance of OWM API object

    Returns:
        A response to message either answering a request or indicating what
        actions were taken
    """

    ## TEXT PREPROCESSING
    # lowercase, strip, and replace whitespace and newline characters with single space
    message = processer.simpleProcessor(message)
    print("(Simply) processed input: ", message)
    # Store default answer as error messae
    answer = ""

    # Look for keyword triggers in the incoming SMS
    
    ## WEATHER
    if re.search("weather", message) and pyowm_object != None:
        answer = weatherAction(message, processer, pyowm_object)
    ## WOLFRAM
    elif "wolfram" in message:
        answer = "get a response from the Wolfram Alpha API"
    ## WIKI
    elif re.search("wiki(pedia)?", message):
        answer = wikipediaAction(message, processer)
    # LIGHTS
    elif re.search("lamps?|lights?", message) and philips_bridge != None:
        answer = lightsAction(message, processer, philips_bridge)

    # the message contains no keywords. Display a help prompt to identify
    # possible commands
    else:
        answer = '''\nStuck? Here are some things you can ask me:\n\n'wolfram' {a question}\n'wiki' {wikipedia request}\n'weather' {place}\n'turn lights off'\n\nNote: some of these features require additional setup '''

    # return the formulated answer
    return answer
