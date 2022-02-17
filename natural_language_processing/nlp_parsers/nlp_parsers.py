import json
from collections import Counter
from typing import Any
import re
import nltk.corpus
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
# need to have java version 8 or later installed ----- MAKE SURE TO MENTION IN REQUIREMENTS.TXT
from tika import parser

class NLP_Parsers:
    """
    Instantiate a parser that has functions to parse various file types
    """

    def __init__(self):
        pass

    @staticmethod
    def _has_digit(word) -> bool:
        """
        Check if a string has a digit in it
        :param str word: string to check
        :return has_digit: stores whether or not string has a number
        :rtype has_digit: bool
        """

        has_digit = any(char.isdigit() for char in word)
        return has_digit

    @staticmethod
    def clean_text(text) -> list[str]:
        """
        Clean given text by making lower case, removing punctuation and special charactars, tokenizing, and lemmetizing words

        :param str text: text to be cleaned
        :return words: list of words after cleaning text
        :rtype words: list[str]
        """

        # make string into all lowercase
        text = text.lower()

        # remove punctuation, white space, and other weird characters
        text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)

        # remove stop words
        stop = stopwords.words('english')
        text = " ".join([word for word in text.split() if word not in (stop)])

        # split text into list of words
        words = nltk.word_tokenize(text)

        # lemmatize words in text
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]

        # remove 'words' that include numbers in them
        words = [word for word in words if not NLP_Parsers._has_digit(word)]

        # return words
        return words

    def json_parser(self, filename) -> dict[str, Any]:
        """
        Function for parsing a json file

        :param str filename: file path of file being passed in
        :return results: dictionary containing occurance of each word and total number of words in the text
        :rtype results: dict[str, Any]
        """

        # read file and extract text
        with open(filename) as f:
            raw = json.load(f)
            text = raw['text']

        # clean text
        words = NLP_Parsers.clean_text(text)
        
        # calculate number of words and count per word
        wc = Counter(words)
        num = len(words)

        # find average sentence length ##################### -----------------------

        # return dictionary of wordcount and numwords
        results = {'wordcount': wc, 'numwords': num}
        return results

    def pdf_parser(self, filename) -> dict[str, Any]:
        """
        Function for parsing a pdf file

        :param str filename: file path of file being passed in
        :return results: dictionary containing occurance of each word and total number of words in the text
        :rtype results: dict[str, Any]
        """

        # read file and extract text
        raw = parser.from_file(filename)
        text = raw['content']

        # clean text
        words = NLP_Parsers.clean_text(text)

        # calculate number of words and count per word
        wc = Counter(words)
        num = len(words)
        
        # return dictionary of wordcount and numwords
        results = {'wordcount': wc, 'numwords': num}
        return results

    def txt_parser(self, filename) -> dict[str, Any]:
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
        words = NLP_Parsers.clean_text(text)

        # calculate number of words and count per word
        wc = Counter(words)
        num = len(words)

        # return dictionary of wordcount and numwords
        results = {'wordcount': wc, 'numwords': num}
        return results