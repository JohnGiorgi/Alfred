import re

PATH_TO_STOPWORDS = 'alfred/resources/stopwords.txt'

def sterilize(text):
    """Sterilize input `text`. Remove proceeding and preeceding spaces, and replace spans of
    multiple spaces with a single space.

    Args:
        text (str): text to sterilize.

    Returns:
        sterilized message `text`.
    """
    return re.sub(r'\s+', r' ', text.strip())

def remove_stopwords(tokens):
    """
    Returns a list of all words in tokens not found in `PATH_TO_STOPWORDS`.

    Args:
        tokens (list): tokens to remove stopwords from.

    Returns:
        `tokens` with stopwords in `PATH_TO_STOPWORDS` removed.
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
