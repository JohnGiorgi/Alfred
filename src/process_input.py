import re
import spacy

from nltk.corpus import stopwords

PATH_TO_STOPWORDS = '../resources/stopwords.txt'

def sterilize(text):
    """Sterilize input text. Remove proceeding and preeceding spaces, lowercase,
    and replace spans of multiple spaces with a single space.

    Args:
        text: text to sterilize

    Returns:
        sterilized message
    """
    return re.sub('\s+', ' ', text.strip())

def remove_stopwords(tokens):
    """
    Returns a list of all words in tokens not found in stopwords

    Args:
        tokens: tokens to remove stopwords from
        stopwords: path to a stopwords text file. Expects each word on its own line

    Returns:
        lst with stopwords removed
    """
    filtered_list = []

    with open(PATH_TO_STOPWORDS, 'r') as f:
        stopwords_list = [x.strip() for x in f.readlines()]
        # use a set, lookup is quicker
        stopwords_set = set(stopwords_list)
        for word in tokens:
            if word not in stopwords_set:
                filtered_list.append(word)
    return filtered_list

def load_spacy_model(disable=False):
    """
    Returns loaded spacy pipeline

    Args:
        disable: a list of pipeline components to disable from loaded spacy
        model. Can signifcantly increase speed.

    Returns:
        spacy pipeline
    """
    # if diable is not false, load spacy model with modified pipeline
    # otherwise, load the default pipeline
    if disable:
        try:
            nlp = spacy.load('en_core_web_sm', disable=disable)
        except:
            print('''[ERROR] You likely pased an invalid disable argument to
                     get_spacy_doc!''')
    else:
        nlp = spacy.load('en_core_web_sm')

    return nlp


def get_spacy_doc(message, disable=False):
    """
    Returns the doc object obtained by running a spacy model on message.

    Args:
        message: message for spacy to process
        disable: a list of pipeline components to disable from loaded spacy
        model. Can signifcantly increase speed.

    Returns:
        spacy doc object
    """
    nlp = load_spacy_model(disable)
    return nlp(message)
