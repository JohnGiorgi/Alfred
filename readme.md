# Alfred

Alfred is a Python application built using the web-framework [Flask](https://github.com/pallets/flask/). Inbound SMS sent to your Twilio phone number are forwarded to Alfred as a HTTP request. Alfred intelligently generates a response (SMS to the sender via a HTTP POST request to Twilio) and an action (e.g.: turning off the lights in your home).

### Table of Contents
1. [Setup](#setup)
  -  [Get Twilio Number](#get-number)
  - [Setup Virtual Environment (Optional)](#virtual-env)
  - [Install and Run](#install)
2. [Connect to services](#connect)
  - [Phillips Hue](#hue)
  - [OWM](#owm)
  - [Nest Learning Thermostat](#nest)
  - [WolframAlpha](#wolfram)
3. [What can you ask Alfred to do?](#ask-alfred)
4. [Changelog](#change-log)

<a name = 'setup'></a>
## Setup

<a name = 'get-number'></a>
### Get a Twilio Number

First you need a Twilio phone number capable of sending and receiving SMS messages. You can get a number with your free trial [here](https://www.twilio.com/try-twilio).

<a name = 'virtual-env'></a>
### Setting up a Virtual Environment (OPTIONAL)

It is recommended that you set up a virtual environment. See [here](https://conda.io/docs/using/envs.html) for how to activate
a `conda` environment. The environment can be activated by calling `source activate <env name>`.

<a name = 'install'></a>
### Install and Run

1. Navigate to the directory you want to save smsbot to, and `git clone` there. Or download the source code as a `.zip`.
2. Activate your environment from the previous step (optional).
3. If you plan on using all features of Alfred, then run `pip install -r requirements.txt` from within the cloned directory. Otherwise take a look at `requirements.txt` and `pip install` the features that you want (`flask`, `twilio` and `nltk` are required).
3. Run the main script: `python src/run_alfred.py`. Note the port reported by Flask on the command line, ex: 'Running on http://XXX.X.X.X:5000/'
4. Install `ngrok` (download [here](https://ngrok.com/)) and add it to your `PATH`.
5. Run ngrok: `ngrok http <port>`, where port would be **5000** from the example above. Note the **forwarding address** reported by ngrok on the command line, ex: 'http://XXXXXXXX.ngrok.io'
6. Copy and past one of the **forwarding addresses** into the "A MESSAGE COMES IN" field on the Twilio dashboard (from the dashboard, click the '#' then your phone number and scroll down to "Messaging"). Make sure the drop down is set to "**Webhook**".

<a name = 'connect'></a>
### Setting up each service

<a name = 'hue'></a>
#### Phillips Hue

If you plan on using the script with the Philips Hue Bridge, there are a few extra steps:
1. Make sure that in `/src/config.ini` you have set `bridgeIP` to the **IP** of your Bridge. Instructions on how to find that [here](https://developers.meethue.com/documentation/getting-started).
2. Before running the script for the first time, press the button on the Hue Bridge. Then, within 30 seconds call the script and pass the `--connectBridge` flag (you only have to do this **once**).
3. That's it. Try texting your Twilio number 'Turn on all the lights please!' to make sure things are working.

*Note, you can also run* `python src/run_alfred.py --setup` *and Alfred will walk you through this process and modify the configuration file for you*.

<a name = 'owm'></a>
#### Weather
Requests for weather information rely on the OpenWeatherMap.org API. An API key is already provided with Alfred, but if you would prefer to use your own sign up [here](https://openweathermap.org/), then go to **API Keys** and copy your key to the config file (at `/src/config.ini`).

<a name = 'nest'></a>
#### Nest Learning Thermostat
Coming soon.

<a name = 'wolfram'></a>
#### WolframAlpha
Coming soon.

<a name = 'ask-alfred'></a>
## What can you ask Alfred to do?

- Example 1: "Turn on the lights" <turns on all lights>
- Example 2: "Turn on the bedroom lights" <turns on all lights in the Phillips hue group 'Bedroom', if this group exists>
- Example 3: "Dim the living room lights" <sets all lights in the Phillips hue group 'Living room' to 15% intensity>
- Example 4: "Set the lights to 50%" <sets all lights to 50% intensity>
- Example 5: "Warm the bedroom lights" <sets all lights in the Phillips hue group 'Bedroom' to the warmest end of the spectrum>
- Example 6: "Set the living room lights blue" <sets all lights in the Phillips hue group 'Living room' to blue>
- Example 7: "Wiki Barack Obama" <returns wiki summary with link>
- Example 8: "What is the weather like in New York City?" <returns weather summary for location>

## Changelog <a name = 'change-log'></a>

**Latest commits**:
- Added the ability to set light colors. Try "Set bedroom lights green"
- Added two new command "Warm the lights" and "Cool the lights"
