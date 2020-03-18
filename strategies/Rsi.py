import numpy as np
from .Portfolio import Portfolio
from .Strategy import Strategy


class Rsi(Strategy):
    '''
    Basic Info and Implementation:
    The relative strength index (RSI) is a momentum indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset. The RSI is displayed as an oscillator (a line graph that moves between two extremes) and can have a reading from 0 to 100.

    What RSI tell us:
    The RSI compares bullish and bearish price momentum plotted against the graph of an asset's price.
Signals are considered overbought when the indicator is above 70% and oversold when the indicator is below 30%.

Formulae:
RSI = 100 * ( x / 1 + x )
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


        @param df:
        @param startdate:
        @param enddate:
        @param dfcol:
        @param window:
        @return:
        '''
        temp = Strategy.slicebydate(df, startdate, enddate)
        temp2 = temp[dfcol].diff()
        profit, loss = temp2.copy(), temp2.copy()
        profit[profit < 0] = 0
        loss[loss > 0] = 0
        profitroll = profit.rolling(window, min_periods=window).mean()
        lossroll = loss.rolling(window, min_periods=window).mean().abs()
        x = profitroll / lossroll
        x = (x / (1 + x))
        temp['rsi'] = (x * 100)
        return temp

    def plotit(self, temp):
        '''


        @param temp:
        @return:
        '''
        temp.plot(x='Date', y='rsi')

    def rsisig(self, df, startdate, enddate, upperlimit, lowerlimit, dfcol, window):
        '''


        @param df:
        @param startdate:
        @param enddate:
        @param upperlimit:
        @param lowerlimit:
        @param dfcol:
        @param window:
        @return:

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
