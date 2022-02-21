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
from statistics import mean
from textblob import TextBlob
# need to have java version 8 or later installed ----- MAKE SURE TO MENTION IN REQUIREMENTS.TXT
from tika import parser

class NLP_Parsers:
    """
    Instantiate a parser that has functions to parse and gather statistics on texts in various file types
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
    def clean_text(text) -> tuple[list[str], str]:
        """
        Clean given text by making lower case, removing punctuation and special charactars, tokenizing, and lemmetizing words

        :param str text: text to be cleaned
        :return words: list of words after cleaning text
        :rtype words: list[str]
        :return text: cleaned full text
        :rtype text: str
        """

        # make string into all lowercase
        text = text.lower()

        # remove punctuation, white space, and other weird characters
        text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)

        # split text into list of words
        words = nltk.word_tokenize(text)

        # remove stop words
        STOP_WORDS = list(stopwords.words('english'))
        STOP_WORDS.append('thats')
        words = [word for word in words if word not in STOP_WORDS]
        text = " ".join([word for word in text.split() if word not in STOP_WORDS])

        # lemmatize words in text
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
        text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])

        # remove 'words' that include numbers in them
        words = [word for word in words if not NLP_Parsers._has_digit(word)]
        text = " ".join([word for word in text.split() if not NLP_Parsers._has_digit(word)])

        # return cleaned list of words and cleaned text as string
        return (words, text)

    @staticmethod
    def statistics(text) -> tuple[float, float]:
        """
        Find average sentence length and average number of unique words per 1000 words
        
        :param str text: text to grab statistics for
        :return avg_sent_length: mean length of sentences in the text
        :rtype avg_sent_length: float
        :return avg_num_unique_words: mean number of unique words per 1000 words in the text
        :rtype avg_num_unique_words: float        
        """

        # split text into list of sentences
        sentences = nltk.tokenize.sent_tokenize(text)

        # find mean sentence length of text
        sentences = [sentence.split() for sentence in sentences]
        avg_sent_length = mean([len(sentence) for sentence in sentences])
        
        # split text per 1000 words
        text_split = text.split()
        split = []
        for i in range(0, len(text_split), 1000):
            split.append(" ".join(text_split[i:i + 1000]))
        
        # find number of unique words per part
        num_unique_words = []
        for part in split:
            # split each part into words
            words = part.split()

            # make list of words in a part into a set to find unique words
            words = set(words)

            # add number of unique words in a part to the list
            num_unique_words.append(len(words))

        # return mean number of unique words per 1000 words
        avg_num_unique_words = mean(num_unique_words)

        # return desired statistics
        return (avg_sent_length, avg_num_unique_words)

    @staticmethod
    def score_text(text, minsub=0.0, maxsub=1.0, minpol=-1.0, maxpol=1.0) -> tuple[Any, Any]:
        """
        Assign polarity and subjectivity scores to texts

        :param list[str] texts: text to score
        :return filtered: texts and their assigned polarity and subjectivity scores
        :rtype filtered: tuple[Any, Any]
        """

        # assign polarity and subjectivity using textblob sentiment
        pol, sub = TextBlob(text).sentiment
        if minpol <= pol <= maxpol and minsub <= sub <= maxsub:
            scores = (pol, sub)

        # return scores
        return scores

    @staticmethod
    def analyze(text) -> dict[str, Any]:
        """
        Clean and gather statistics for a given text

        :param str text: text to analyze
        :return results: dictionary of statistics about text
        :rtype results: dict[str, Any]
        """

        # clean text
        words, cleaned_text = NLP_Parsers.clean_text(text)
        
        # calculate number of words and count per word
        wc = Counter(words)
        num = len(words)

        # average sentence length and average number of unique words
        sl, uw = NLP_Parsers.statistics(text)

        # sentiment of original and cleaned text in terms of polarity and subjectivity
        score = NLP_Parsers.score_text(text)
        score_cleaned = NLP_Parsers.score_text(cleaned_text)

        # return dictionary of statistics
        results = {'word_count': wc, 'num_words': num, 'avg_sent_length': sl, 'unique_words': uw, 'sentiment': score, 'cleaned_sentiment': score_cleaned}
        return results

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

        # return dictionary of statistics
        results = NLP_Parsers.analyze(text)
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

        # return dictionary of statistics
        results = NLP_Parsers.analyze(text)
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
        
        # return dictionary of statistics
        results = NLP_Parsers.analyze(text)
        return results