from generate_response import get_reply

def testing(philips_bridge, pyowm_object):
    """
    This method runs a testing loop, which prompts for input until user
    enters 'exit'. The intention is to be able to test changes to Alfred
    through the command line instead of via SMS.
    """
    user_input = ""
    while user_input.lower() != 'exit':
        user_input = input("Please enter a request: ")
        print("\nRESPONSE\n----------------------------",
        get_reply(user_input, philips_bridge, pyowm_object),
        "\n",
        sep = "\n")
