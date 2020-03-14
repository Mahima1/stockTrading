import matplotlib.pyplot as plt
import numpy as np

from .Strategy import Strategy
from .Portfolio import Portfolio

from .MA import MA


class MACD(Strategy, MA):
    Strategy.names.append('MACD')
    '''
Basic Info and Implementation:
Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator
that shows the relationship between two moving averages of a security’s price.

The MACD is calculated by subtracting the 26-period Moving Average (MA) from the 12-period MA.

MACD tell us:
MACD triggers technical signals when it crosses above (to buy) or below (to sell) its signal line.
The speed of crossovers is also taken as a signal of a market is overbought or oversold.
The MACD has a positive value whenever the 12-period EMA (blue) is above the 26-period MA (red) 
and a negative value when the 12-period EMA is below the 26-period MA.

Formulae:
MACD=12-Period MA − 26-Period MA


    '''

    def __init__(self, window1, window2):
        super(Strategy, self).__init__()
        super(MA, self).__init__()
        self.window1 = window1
        self.window2 = window2

    def macd(self, df, startdate, enddate, dfcol, window1, window2):
        '''

        @param df:
        @param startdate:
        @param enddate:
        @param dfcol:
        @param window1:
        @param window2:
        @return:
        '''
        t1 = MA.moving_average(df, startdate, enddate, dfcol, window1)
        t2 = MA.moving_average(df, startdate, enddate, dfcol, window2)
        return t1, t2

    def plotit(self, t1, t2):
        '''


        @param t1:
        @param t2:
        @return:
        '''
        plt.plot(t1['Date'], t1['roll'])
        plt.plot(t2['Date'], t2['roll'])

    def macdsig(self, df, startdate, enddate, dfcol, window1, window2):
        q1, q2 = MACD.macd(df, startdate, enddate, dfcol, window1, window2)
        q1['diff'] = q1['roll'] - q2['roll']
        q1['shift'] = (q1['diff'].shift(1))
        q1['multiple'] = q1['diff'] * q1['shift']
        mask = q1['multiple'] < 0
        mask1 = q1['shift'] > 0
        where1 = np.where(mask1, 'buy', 'sell')
        q1['signal'] = np.where(mask, where1, 'None')
        q1 = q1.drop(columns=['diff', 'shift', 'multiple'])
        return q1

    def macdoptimize(self, df, startdate, enddate, dfcol, arr):
        '''


        @param df:
        @param startdate:
        @param enddate:
        @param dfcol:
        @param arr:
        @return:
        '''
        maxprofit = windowshort = windowlong = 0
        count1 = arr[0][1] - arr[0][0] + 1
        count2 = arr[1][1] - arr[1][0] + 1
        w1 = arr[0][0]
        for p in range(count1):
            w2 = arr[1][0]
            for e in range(count2):
                t = MACD.macdsig(df, startdate, enddate, dfcol, w1, w2)
                net = Portfolio.pfmanage(t, 'Close')
                if maxprofit < net:
                    maxprofit = net
                    windowshort = w1
                    windowlong = w2
                w2 += 1
            w1 += 1
        return [maxprofit, windowshort, windowlong, 'MACD']
