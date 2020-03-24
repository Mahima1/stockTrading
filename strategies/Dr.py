from .Strategy import Strategy


class Dr(Strategy):
    Strategy.names.append('Daily_return')

    def __init__(self):
        super(Strategy, self).__init__()
        pass

    @classmethod
    def daily_return(cls, df, dfcol):
        df[dfcol + '_dr'] = ((df[dfcol].shift(1) - df[dfcol]) / df[dfcol]) * 100
        return df
