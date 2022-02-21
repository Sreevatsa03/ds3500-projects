"""
filename: nlp.py
description: a reusable nlp framework
author: Sreevatsa Nukala
"""
from collections import Counter, defaultdict
import random as rand
import matplotlib.pyplot as plt
from typing import Any, Callable

class NLP:
    """
    Instantiate natural language processing / text analysis on given texts
    """

    def __init__(self):
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(filename) -> dict[str, Any]:
        """
        Default parsing method that assumes text file and outputs dictionary containing basic statistics of text

        :param str filename: file path of file being passed in
        :return results: dictionary containing occurance of each word and total number of words in the text
        :rtype results: dict[str, Any]
        """

        # read file and extract text
        with open(filename) as f:
            text = f.read()
        
        # split text into list of words
        words = text.split(" ")

        # calculate number of words and count per word
        wc = Counter(words)
        num = len(words)

        # return dictionary of wordcount and numwords
        results = {'word_count': wc, 'num_words': num}
        return results

    @staticmethod
    def polarity_subjectivity_lists(scored_text) -> tuple[list[Any], list[Any]]:
        """
        Find polarity and subjectivity for each body of text

        :param scored_text: dictionary of polarity and subjectivity scores for multiple texts
        :type scored_text: dict[str, tuple[Any, Any]] 
        :return subjectivity: list of subjectivity scores
        :rtype polarity: list[Any]
        :return polarity: list of polarity scores
        :rtype polarity: list[Any]
        """

        scores = scored_text.values()
        polarity = [x[0] for x in scores]
        subjectivity = [x[1] for x in scores]
        return (subjectivity, polarity)

    def load_text(self, filename, label=None, parser=None) -> None:
        """
        Load one text into the NLP object\ 
        Parses a given file and adds its basic statistics (wordcount and numwords) to dictionary for further analysis

        :param str filename: file path of file being passed in
        :param str label: label of the loaded text in meta dictionary
        :param parser: parser you want to use to pre-process your file
        :type parser: Callable[[str], dict[str, Any]]
        """

        # check if custom parser is used
        if parser is None:
            # use default parser if no parser is passed in
            results = NLP._default_parser(filename)
        else:
            # else use custom parser
            results = parser(filename)

        # if no label use file name as label
        if label is None:
            label = filename
        
        # add results of parsing to state stored dictionary
        for key, val in results.items():
            self.data[key][label] = val

    def compare_num_words(self) -> None:
        """
        Create bar chart of texts and their total number of words
        """
        
        num_words = self.data['num_words']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()