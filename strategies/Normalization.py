from .Strategy import Strategy


class Normalization(Strategy):
    Strategy.names.append('Normalization')

    def __init__(self):
        super(Strategy, self).__init__()

    @classmethod
    def norm(cls, df, dfcol):
        df[dfcol + 'norm'] = df[dfcol] / df[dfcol].iloc[0]
        return df
