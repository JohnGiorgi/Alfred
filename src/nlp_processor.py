import re
from nltk import tokenize

class NLProcessor:
    '''Natural language processer class'''
    def __init__(self):
        # load any external dependencies here
        pass
    def simpleProcessor(self, text):
        return re.sub('\s+', ' ', text.lower().strip())

    def tokenize(self, text):
        return tokenize.wordpunct_tokenize(re.sub('\s+', ' ', text))

    def stopwordFilter(self, lst, stopwords):
        """
        Returns a list    all words in lst not in stopwords

        Args:
            lst: list to remove stopwords from
            stopwords: path to a stopwords text file. Expects each word on its own line

        Returns:
            lst with stopwords removed
        """

        filtered_list = []

        with open(stopwords, 'r') as f:
            stopwords_list = [x.strip() for x in f.readlines()]
            # use a set, lookup is quicker
            stopwords_set = set(stopwords_list)
            for word in lst:
                if word not in stopwords_set:
                    filtered_list.append(word)
        return filtered_list
