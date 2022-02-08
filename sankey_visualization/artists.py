from make_sankey import MakeSankey
import pandas as pd

class Artists():

    def __init__(self):
        pass

    def read_json(self, filename):
        """Read json data into dataframe"""

        # read data into df
        df = pd.read_json(filename)

        # convert from birth year to birth decade
        df['BirthDecade'] = df.BeginDate - (df.BeginDate % 10)
        df.drop(df.columns.difference(['Nationality', 'Gender', 'BirthDecade']), 1, inplace=True)

        # return df
        return df

    def aggregate_df(self, df, src, tar, vals, filter_threshold=20):
        """Group dataframe by given src and tar columns\n
        Threshold dataframe to only include artists with count >= a given threshold value"""

        # groupby function on df
        grouped = df.groupby([src, tar]).size().reset_index(name=vals)

        # threshold and return df
        return grouped[grouped[vals] >= filter_threshold]
    
    def make_sankeys(self, df, src_list, tar_list, vals):
        """Make multiple sankey diagrams from lists of source and target columns"""

        # loop through src and tar lists
        for i in range(len(src_list)):
            # aggregate and clean data
            grouped = self.aggregate_df(df, src_list[i], tar_list[i], vals, 25)
            if tar_list[i] == 'BirthDecade':
                grouped = grouped[grouped[tar_list[i]] != 0]

            # make sankey diagram
            ms = MakeSankey(grouped)
            ms.make_sankey(src_list[i], tar_list[i], vals)

def main():
    # create artists object to read data and make dataframe
    artists = Artists()

    # read data into dataframe
    artists_df = artists.read_json('Artists.json')

    # make sankeys
    artists.make_sankeys(artists_df, ['Nationality', 'Nationality', 'Gender'], ['BirthDecade', 'Gender', 'BirthDecade'], 'Count')

if __name__ == "__main__":
    main()
