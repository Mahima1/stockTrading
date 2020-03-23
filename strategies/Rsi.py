import numpy as np
from .Portfolio import Portfolio
from .Strategy import Strategy
from .Dr import Dr


class Rsi(Strategy):
    '''
    Basic Info and Implementation:
    The relative strength index (RSI) is a momentum indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. The RSI is displayed as an oscillator (a line graph that moves between two extremes) and can have a reading from 0 to 100.

    What RSI tell us:
    The RSI compares bullish and bearish price momentum plotted against the graph of an asset's price.
    Signals are considered overbought when the indicator is above 70% and oversold when the indicator is below 30%.

    Formulae:
    RSI = 100 * ( x / (1 + x ) )
    x = average gain / average loss

    '''
    Strategy.names.append('Rsi')

    def __init__(self, dfcol, window):
        super(Strategy, self).__init__()
        super(Strategy, self).__init__()
        self.dfcol = dfcol
        self.window = window

    def rsi(self, df, startdate, enddate, dfcol, window):
        '''
        This func first calculates daily return of column as parameter for dfcol then it takes avg gain and avg loss by first filtering positive daily retuns and negative in different dataframes then calculates moving averages for both. The ratio of  averages is our x in the formulae then the dataframe with 'rsi' column is returned with the results stored.


        @param df: Dataframe with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param window: int
        @return: Dataframe with TYPICAL PRICE, STD (standard deviation), UPPER BAND, LOWER BAND columns added into it

        '''
        temp = Strategy.slicebydate(df, startdate, enddate)
        # temp = df.copy()
        temp2 = Dr.daily_return(dfcol)
        mask = temp2[dfcol + '_dr'] < 0
        mask1 = temp2[dfcol + '_dr'] >= 0
        temp['loss'] = np.where(mask, abs(temp2), 0)
        temp['profit'] = np.where(mask1, temp2, 0)
        profitroll = temp['profit'].rolling(window, min_periods=window).mean()
        lossroll = temp['loss'].rolling(window, min_periods=window).mean()
        x = profitroll / lossroll
        y = (x / (1 + x))
        temp['rsi'] = (y * 100)
        return temp

    def plotit(self, temp):
        '''
        Function for plotting bands in a time series graph.
        @param temp: Dataframe returned from Bollinger_bands function.
        @return: void
        '''

        temp.plot(x='Date', y='rsi')

    def rsisig(self, df, startdate, enddate, upperlimit, lowerlimit, dfcol, window):
        '''
        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param upperlimit: int , upper limit after which security can be called overbrought 
        @param lowerlimit: lower limit after which security can be called oversold
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param window: int ,
        @return: Dataframe with 'SIGNAL' column added to it

        '''
        t = Rsi.rsi(df, startdate, enddate, dfcol, window)
        mask = t['rsi'] <= lowerlimit
        mask1 = t['rsi'] >= upperlimit
        t['signal'] = np.where(mask, 'buy', (np.where(mask1, 'sell', 'None')))
        return t

    def rsioptimize(self, df, startdate, enddate, dfcol, arr):
        '''


        @param df:
        @param startdate:
        @param enddate:
        @param dfcol:
        @param arr:
        @return:

        '''
        maxprofit = upperlimit = lowerlimit = window = 0
        count1 = arr[0][1] - arr[0][0] + 1
        count2 = arr[1][1] - arr[1][0] + 1
        count3 = arr[2][1] - arr[2][0] + 1
        up = arr[0][0]
        for p in range(count1):
            low = arr[1][0]
            for e in range(count2):
                w = arr[2][0]
                for r in range(count3):
                    t = Rsi.rsisig(df, startdate, enddate, up, low, dfcol, w)
                    net = Portfolio.pfmanage(t, 'Close')
                    if maxprofit < net:
                        maxprofit = net
                        upperlimit = up
                        lowerlimit = low
                        window = w
                    w += 1
                low += 1
            up += 1
        return [maxprofit, upperlimit, lowerlimit, window, 'Rsi']
