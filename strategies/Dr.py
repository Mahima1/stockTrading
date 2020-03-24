from .Strategy import Strategy


class Dr(Strategy):
    Strategy.names.append('Daily_return')

    # def __init__(self, dfcol):
    #     super(Strategy, self).__init__()
    #     self.dfcol = dfcol
    def __init__(self):
        super(Strategy, self).__init__()

    def daily_return(self, df, dfcol):
        # z=Strategy.slicebydate(df,startdate,enddate)
        df[dfcol + '_dr'] = ((df[dfcol].shift(1) - df[dfcol]) / df[dfcol]) * 100
        return df
