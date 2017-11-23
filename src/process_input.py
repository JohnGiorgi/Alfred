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
    return re.sub('\s+', ' ', text.lower().strip())

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
