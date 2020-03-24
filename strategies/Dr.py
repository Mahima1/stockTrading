from .Strategy import Strategy


class Dr(Strategy):
    Strategy.names.append('Daily_return')

    def __init__(self):
        super(Strategy, self).__init__()

    def daily_return(self, df, dfcol):
        df[dfcol + '_dr'] = ((df[dfcol].shift(1) - df[dfcol]) / df[dfcol]) * 100
        return df
