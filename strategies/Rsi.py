import numpy as np

from stock_trading.strategies.Dr import Dr
from stock_trading.strategies.Portfolio import Portfolio
from stock_trading.strategies.Strategy import Strategy


class Rsi(Strategy):
    """
    Basic Info and Implementation:
    The relative strength index (RSI) is a momentum indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. The RSI is displayed as an oscillator (a line graph that moves between two extremes) and can have a reading from 0 to 100.

    What RSI tell us:
    The RSI compares bullish and bearish price momentum plotted against the graph of an asset's price.
    Signals are considered overbought when the indicator is above 70% and oversold when the indicator is below 30%.

    Formulae:
    RSI = 100 * ( x / (1 + x ) )
    x = average gain / average loss

    """
    Strategy.names.append('Rsi')

    def __init__(self):
        super(Strategy, self).__init__()

    @classmethod
    def rsi(cls, df, start_date, end_date, dfcol, window):
        """
        This func first calculates daily return of column as parameter for dfcol then it takes avg gain and avg loss by first filtering positive daily retuns and negative in different dataframes then calculates moving averages for both. The ratio of  averages is our x in the formulae then the dataframe with 'rsi' column is returned with the results stored.


        @param df: Dataframe with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param start_date: Date ('YYYY-MM-DD')
        @param end_date: Date ('YYYY-MM-DD')
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param window: int
        @return: Dataframe with TYPICAL PRICE, STD (standard deviation), UPPER BAND, LOWER BAND columns added into it

        """
        temp = Strategy.slicebydate(df, start_date, end_date)
        temp2 = Dr.daily_return(temp, dfcol)
        mask = temp2[dfcol + '_dr'] < 0
        mask1 = temp2[dfcol + '_dr'] >= 0
        temp['loss'] = np.where(mask, abs(temp2[dfcol + '_dr']), 0)
        temp['profit'] = np.where(mask1, temp2[dfcol + '_dr'], 0)
        profitroll = temp['profit'].rolling(window, min_periods=1).mean()
        lossroll = temp['loss'].rolling(window, min_periods=1).mean()
        x = profitroll / lossroll
        y = (x / (1 + x))
        temp['rsi'] = (y * 100)
        return temp

    @classmethod
    def plotit(cls, temp):
        """
        Function for plotting bands in a time series graph.
        @param temp: Dataframe returned from Bollinger_bands function.
        @return: void
        """

        temp.plot(x='Date', y='rsi')

    @classmethod
    def rsisig(cls, df, start_date, end_date, upperlimit, lowerlimit, dfcol, window):
        """
        Uses dataframe returned from rsi func to get upper rand lower bands then we compare 'rsi' values
        with those bands and generate signal of sell as rsi values surpasses upper and buy  if declines below lower.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param start_date: Date ('YYYY-MM-DD')
        @param end_date: Date ('YYYY-MM-DD')
        @param upperlimit: int , upper limit after which security can be called overbrought (typically 70)
        @param lowerlimit: lower limit after which security can be called oversold (typically 30)
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param window: int,
        @return: Dataframe with 'SIGNAL' column added to it

        """
        t = Rsi.rsi(df, start_date, end_date, dfcol, window)
        mask = t['rsi'] <= lowerlimit
        mask1 = t['rsi'] >= upperlimit
        t['signal'] = np.where(mask, 'buy', (np.where(mask1, 'sell', 'None')))
        return t

    @classmethod
    def rsioptimize(cls, df, start_date, end_date, dfcol, arr):
        """
    This function finds best performing window (n) and upper limit (u) and lower limit (l) by calculating profits while iterating over values of n ,u and l in the range we have provided. It uses 'rsisig' function which in turn uses 'Rsi' function
        to generate signals and calculate profits for every value of n , u, l.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param start_date: Date ('YYYY-MM-DD')
        @param end_date: Date ('YYYY-MM-DD')
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param arr: arr is list of lists of the form [[startrange,endrange], [startrange,endrange]] where lists inside are in order
        of window and factor , we could use this type of list too [step,+-range] but here for simplicity we assumed step
        is always integer 1 and hence we are not changing values by 0.1 or any other float number.

        @return: list ['maxprofit=', 'upperlimit=', 'lowerlimit=', 'window=','Rsi']

        """
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
                    t = Rsi.rsisig(df, start_date, end_date, up, low, dfcol, w)
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
