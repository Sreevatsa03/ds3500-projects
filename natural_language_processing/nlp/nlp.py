"""
filename: nlp.py
description: a reusable nlp framework
author: Sreevatsa Nukala
"""
from collections import Counter, defaultdict
import random as rand
import matplotlib.pyplot as plt

class NLP:

    version = "0.01"

    def __init__(self):
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(filename):
        results = {
            'wordcount': Counter("to be or not to be".split(" ")),
            'numwords': rand.randrange(10, 50)
        }
        
        return results

    def load_text(self, filename, label=None, parser=None):
        if parser is None:
            results = NLP._default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename
        
        for key, val in results.items():
            self.data[key][label] = val

    def compare_num_words(self):
        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()