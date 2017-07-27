# Alfred

A simple Flask app written in Python. Incoming SMS sent to your Twilio phone number are routed to the app,
which intelligently generates a response (SMS to the sender) and an action (ex: turning off the lights in your home).

## Setup

### Get a Twilio Number

First you need a Twilio phone number capable of sending and receiving SMS messages. You can get a number with your free trial [here](https://www.twilio.com/try-twilio).

### Setting up a Virtual Environment (OPTIONAL)

It is recommended that you set up a virtual environment. See [here](https://conda.io/docs/using/envs.html) for how to activate
a `conda` environment. The environment can be activated by calling `source activate <env name>`.

### Install and Run

1. Navigate to the directory you want to save smsbot to, and `git clone` there. Or download the source code as a `.zip`.
2. Activate your enviornment from the previous step (optional).
3. If you plan on using all features of Alfred, then run `pip install -r requirements.txt` from within the cloned directory. Otherwise take a look at `requirements.txt` and `pip install` the features that you want (`flask`, `twilio` and `nltk` are required).
3. Run the main script: `python path/to/run_alfred.py`. Note the port reported by Flask on the command line, ex: 'Running on http://XXX.X.X.X:5000/'
4. Install `ngrok` (download [here](https://ngrok.com/)) and add it to your `PATH`.
5. Run ngrok: `ngrok http <port>`, where port would be **5000** from the example above. Note the **forwarding address** reported by ngrok on the command line, ex: 'http://XXXXXXXX.ngrok.io'
6. Copy and past one of the **forwarding addresses** into the "A MESSAGE COMES IN" field on the Twilio dashboard (from the dashboard, click the '#' then your phone number and scroll down to "Messaging"). Make sure the drop down is set to "**Webhook**".

### Getting API Keys

#### Weather
Requests for weather information rely on the OpenWeatherMap.org API. An API key is already provided with Alfred, but if you would prefer to use your own sign up [here](https://openweathermap.org/), then go to **API Keys** and copy your key to
the config file (at `/main/resources/config.ini`).

#### WolframAlpha
Coming soon.

## Notes

If you plan on using the script with the Philips Hue Bridge, there are a few extra steps:
1. Make sure that in `/main/resources/config.ini` you have set `bridgeIP` to the **IP** of your Bridge. Instructions on how to find that [here](https://developers.meethue.com/documentation/getting-started).
2. Before running the script for the first time, press the button on the Hue Bridge. Then, within 30 seconds call the script and pass the `--connectBridge` flag (you only have to do this **once**).
3. That's it. Try texting your Twilio number 'Turn on all the lights please!' to make sure things are working.

## What can you ask Alfred to do?

Example 1: "Turn on the lights" <turns on all lights>
Example 2: "Turn on the bedroom lights" <turns on all lights in the Phillips hue group 'Bedroom', if this group exists>
Example 3: "Dim the living room lights" <sets all lights in the Phillips hue group 'Living room' to 15% intensity>
Example 4: "Set the lights to 50%" <sets all lights to 50% intensity>
Example 5: "Wiki Barack Obama" <returns wiki summary with link>
Example 6: "What is the weather like in New York City?" <returns weather summary for location>

## Changelog

- 1.0: Initial commit
- 1.0.1: Changed how Alfred deals with rooms (Phillips hue calls these 'Groups'). If a group name that is present on your bridge is mentioned in the SMS sent to Alfred, then all actions occur to lights in this group. E.g. "Turn lights on in the bedroom" turns on all lights in the group 'Bedroom' (case-insensitive)
