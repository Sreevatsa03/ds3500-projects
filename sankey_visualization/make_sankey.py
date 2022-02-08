import pandas as pd
import plotly.graph_objects as go

class MakeSankey():
    """Make sankey diagram from given DataFrame"""

    def __init__(self, df):
        self.df = df

    def code_mapping(self, src, tar):
        """Map labels in src and tar columns to integers"""

        labels = list(self.df[src]) + list(self.df[tar])
        # labels = sorted(list(set(labels)))
        
        codes = list(range(len(labels)))

        lcmap = dict(zip(labels, codes))

        self.df = self.df.replace({src: lcmap, tar: lcmap})

        return labels

    def make_sankey(self, src, tar, vals=None, **kwargs):
        """Plot sankey diagram"""

        labels = self.code_mapping(src, tar)

        if vals:
            value = self.df[vals]
        else:
            value = [1] * self.df.shape[0]

        link = dict(source=self.df[src], target=self.df[tar], value=value)

        pad = kwargs.get('pad', 100)
        thickness = kwargs.get('thickness', 10)
        line_color = kwargs.get('line_color', 'black')
        line_width = kwargs.get('line_width', 2)
        node = dict(label=labels, pad=pad, thickness=thickness, line={'color': line_color, 'width': line_width})

        sk = go.Sankey(link=link, node=node)
        fig = go.Figure(sk)
        fig.show()
