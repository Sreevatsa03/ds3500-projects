import pandas as pd
import plotly.graph_objects as go
from typing import Any

class Make_Sankey:
    """
    Create a sankey diagram from a given DataFrame

    :param df: data to create sankey diagram from
    :type df: DataFrame
    """

    def __init__(self, df) -> None:
        self.df = df

    def code_mapping(self, src, tar) -> list[str]:
        """
        Map labels in source and target columns of DataFrame to integers and return list of labels

        :param ``str`` src: label of source column in DataFrame
        :param ``str`` tar: label of target column in DataFrame
        :return labels: list of labels to use in sankey diagram
        :rtype labels: ``list[str]``
        """

        # define list of labels
        labels = list(self.df[src]) + list(self.df[tar])
        # labels = sorted(list(set(labels)))
        
        # define list of codes for code mapping
        codes = list(range(len(labels)))
        
        # code map
        lcmap = dict(zip(labels, codes))

        # use code map
        self.df = self.df.replace({src: lcmap, tar: lcmap})

        # return list of labels
        return labels

    def make_sankey(self, src, tar, vals=None, **kwargs) -> None:
        r"""
        Plot sankey diagram
        
        :param ``str`` src: label of source column in DataFrame
        :param ``str`` tar: label of target column in DataFrame
        :param ``str`` vals: label of values column in DataFrame
        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *pad* (``int``, ``float``) --
            sets the padding (in px) between the nodes
            * *thickness* (``int``, ``float``) --
            sets the thickness (in px) of the nodes
            * *line_color* (``str``) --
            sets the color of the line around each link
            * *line_width* (``int``, ``float``) --
            sets the width (in px) of the line around each link
        """

        # get list of labels and code map given DataFrame
        labels = self.code_mapping(src, tar)

        # grab vals if vals column is not specified
        if vals:
            value = self.df[vals]
        else:
            value = [1] * self.df.shape[0]

        # create dictionary of links in diagram
        link = dict(source=self.df[src], target=self.df[tar], value=value)

        # customize nodes and links of sankey diagram
        pad = kwargs.get('pad', 100)
        thickness = kwargs.get('thickness', 10)
        line_color = kwargs.get('line_color', 'black')
        line_width = kwargs.get('line_width', 2)
        node = dict(label=labels, pad=pad, thickness=thickness, line={'color': line_color, 'width': line_width})

        # plot and show sankey diagram
        sk = go.Sankey(link=link, node=node, valueformat='.3r')
        fig = go.Figure(sk)
        fig.write_html("sankey.html")
