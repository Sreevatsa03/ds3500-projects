import json
from collections import Counter

class NLP_Parsers():

    def __init__(self):
        pass

    def json_parser(self, filename):
        with open(filename) as f:
            raw = json.load(f)
            text = raw['text']
            words = text.split(" ")

        wc = Counter(words)
        num = len(words)

        return {'wordcount': wc, 'numwords': num}
