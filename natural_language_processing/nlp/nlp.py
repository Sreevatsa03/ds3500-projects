"""
filename: nlp.py
description: a reusable nlp framework
author: Sreevatsa Nukala
"""
from collections import Counter, defaultdict
from typing import Any, Callable
import matplotlib.pyplot as plt
from nlp.make_sankey import Make_Sankey
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

class NLP:
    """
    Instantiate natural language processing / text analysis on given texts
    """

    def __init__(self) -> None:
        self.data = defaultdict(dict)

    @staticmethod
    def _default_parser(filename) -> dict[str, Any]:
        """
        Default parsing method that assumes text file and outputs dictionary containing basic statistics of text

        :param ``str`` filename: file path of file being passed in
        :return results: dictionary containing occurance of each word and total number of words in the text
        :rtype results: ``dict[str, Any]``
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

    def load_text(self, filename, label=None, parser=None, stop_words=None) -> None:
        """
        Load one text into the NLP object\ 
        Parses a given file and adds its basic statistics (wordcount and numwords) to dictionary for further analysis

        :param ``str`` filename: file path of file being passed in
        :param ``str`` label: label of the loaded text in meta dictionary
        :param parser: parser you want to use to pre-process your file
        :type parser: ``Callable[[str], dict[str, Any]]``
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

        plt.xlabel("Text")
        plt.ylabel("Number of Words")
        plt.title("Number of Words per Text")
        plt.savefig("numwords.png")
    
    def most_common(self, k, is_weighted=False) -> list[tuple[str, int]]:
        """
        Generate sankey diagram between texts and set of commonly used words across all texts

        :param ``int`` k: top k most common words
        :param ``bool`` is_weighted: indicates whether to use weighted word count
        :return most_common: list of most common words across texts
        :rtype most_common: ``list[tuple[str, int]]``
        """

        # create counter for word count across texts
        count = Counter([])

        if not is_weighted:
            for value in self.data['word_count'].values():
                count += value
        else:
            for value in self.data['weighted_word_count'].values():
                count += value

        # return most common words
        most_common = [common for common in count.most_common(k)]
        return most_common

    def word_count_sankey(self, word_list=None, k=5, is_weighted=False) -> None:
        """
        Map each text to words using a sankey diagram, where the thickness of the line is the number of times that word occurs in the text.

        :param word_list: optional user-specified list of words to map to texts
        :type word_list: ``list[str]``
        :param ``int`` k: top k most common words
        :param ``bool`` is_weighted: indicates whether to use weighted word count
        """
        
        # set word list to list of k most common words if no word list is given 
        if word_list is None:
            word_list = [word[0] for word in self.most_common(k, is_weighted)]

        # get lists of data to use in DataFrame
        text_data = []
        word_data = []
        count_data = []
        for word in word_list:
            if not is_weighted:
                for key, value in self.data['word_count'].items():
                    text_data.append(str(key))
                    word_data.append(word)
                    count_data.append(value[word])
            else:
                for key, value in self.data['weighted_word_count'].items():
                    text_data.append(str(key))
                    word_data.append(word)
                    count_data.append(value[word])

        # create DataFrame for making sankey diagram
        word_count_df = pd.DataFrame(data={'Text': text_data, 'Word': word_data, 'Count': count_data})

        # plot sankey diagram
        sankey = Make_Sankey(word_count_df)
        sankey.make_sankey('Text', 'Word', 'Count')

    def sub_pol_lists(self, is_cleaned=False) -> tuple[list[Any], list[Any]]:
        """
        Get lists of polarity and subjectivity for each body of text

        :param ``bool`` is_cleaned: indicate whether sentiment scores for cleaned or original text should be used
        :return subjectivity: list of subjectivity scores
        :rtype polarity: ``list[Any]``
        :return polarity: list of polarity scores
        :rtype polarity: ``list[Any]``
        """

        # scores = scored_text.values()
        if not is_cleaned:
            polarity = [value[0] for value in self.data['sentiment'].values()]
            subjectivity = [value[1] for value in self.data['sentiment'].values()]
        else:
            polarity = [value[0] for value in self.data['cleaned_sentiment'].values()]
            subjectivity = [value[1] for value in self.data['cleaned_sentiment'].values()]
        return (subjectivity, polarity)

    def sentiment_analysis(self) -> None:
        """
        Plot sentiments of each text (cleaned and uncleaned)
        """
        # get polarity and subjectivity lists
        sub_pol = self.sub_pol_lists(False)
        sub_pol_cleaned = self.sub_pol_lists(True)

        # create DataFrame to plot
        df = pd.DataFrame({'Text': list(self.data['sentiment'].keys()), 'Sub': sub_pol[0], 'Pol': sub_pol[1], 'Cleaned_Sub': sub_pol_cleaned[0], 'Cleaned_Pol': sub_pol_cleaned[1]})
        
        # plot figure
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Original Texts", "Cleaned Texts"),
            shared_yaxes=True
        )

        fig.add_trace(
            go.Scatter(x=df['Sub'], y=df['Pol'], mode="markers+text", text=df['Text'], textposition='bottom left'), 
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Cleaned_Sub'], y=df['Cleaned_Pol'], mode="markers+text", text=df['Text'], textposition='bottom left'), 
            row=1, col=2
        )

        fig.update_xaxes(title_text="Subjectivity", range=[0.3, 0.55], row=1, col=1)
        fig.update_xaxes(title_text="Subjectivity", range=[0.3, 0.55], row=1, col=2)
        fig.update_yaxes(title_text="Polarity", row=1, col=1)

        fig.update_layout(
            showlegend=False,
            height=750, width=1500,
            title_text="Sentiment Analysis"
        )

        # display plot
        fig.write_html("sentiment.html")

    def sentence_length_and_unique_words_comparison(self) -> None:
        """
        Plot bar chart of average sentence lengths in texts
        """

        # plot figure
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("Average Sentence Length", "Average Number of Unique Words per 1000 Words"),
            shared_xaxes=True,
            vertical_spacing=0.075
        )

        fig.add_trace(
            go.Bar(x=list(self.data['avg_sent_length'].keys()), y=list(self.data['avg_sent_length'].values())), 
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(x=list(self.data['unique_words'].keys()), y=list(self.data['unique_words'].values())), 
            row=2, col=1
        )

        fig.update_xaxes(title_text="Texts", tickfont=dict(size=15), row=2, col=1)
        fig.update_yaxes(title_text="Avg Sentence Length (# Words)", row=1, col=1)
        fig.update_yaxes(title_text="Avg Number of Unique Words", row=2, col=1)

        fig.update_layout(
            showlegend=False,
            height=700, width=700,
            title_text="Comparisons: Sentence Length and Number of Unique Words"
        )

        # display plot
        fig.write_html("comparisons.html")

    def plot_heaps_law(self):
        """
        Plot Heaps' Law for each text
        """

        # create lists of data for plotting
        total_data = []
        unique_data = []
        text_data = []
        for key, value in self.data['heaps_law'].items():
            total_data.append(value[0])
            unique_data.append(value[1])
            text_data.append(str(key))

        # create DataFrame for each text
        df_paper1 = pd.DataFrame({'total_words': total_data[0], 'num_unique_words': unique_data[0], 'text': [text_data[0]]*len(total_data[0])})
        df_paper2 = pd.DataFrame({'total_words': total_data[1], 'num_unique_words': unique_data[1], 'text': [text_data[1]]*len(total_data[1])})
        df_paper3 = pd.DataFrame({'total_words': total_data[2], 'num_unique_words': unique_data[2], 'text': [text_data[2]]*len(total_data[2])})
        df_article1 = pd.DataFrame({'total_words': total_data[3], 'num_unique_words': unique_data[3], 'text': [text_data[3]]*len(total_data[3])})
        df_article2 = pd.DataFrame({'total_words': total_data[4], 'num_unique_words': unique_data[4], 'text': [text_data[4]]*len(total_data[4])})
        df_article3 = pd.DataFrame({'total_words': total_data[5], 'num_unique_words': unique_data[5], 'text': [text_data[5]]*len(total_data[5])})
        
        # concatenate DataFrames
        df = pd.concat([df_paper1, df_paper2, df_paper3, df_article1, df_article2, df_article3], ignore_index=True)

        # create subplots using facets in plotly
        fig = px.scatter(
            df, x='total_words', y='num_unique_words', 
            title="Heaps' Law for Each Text", labels={"total_words": "Total Number of Words", "num_unique_words": "Number of Unique Words", "text": "Text"}, 
            facet_col='text', color='text', facet_col_wrap=3, log_x=True, log_y=True, trendline="ols", trendline_options=dict(log_x=True, log_y=True), trendline_color_override='black')

        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        # display plot
        fig.write_html("heaps.html")