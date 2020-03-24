import matplotlib.pyplot as plt
import numpy as np

from .MA import MA
from .Portfolio import Portfolio
from .Strategy import Strategy


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
and a negative value when the 12-period MA is below the 26-period MA.

Formulae:
MACD = 12-Period MA − 26-Period MA

where: 
MA is moving average

    '''

    def __init__(self):
        super(Strategy, self).__init__()
        super(MA, self).__init__()

    def macd(self, df, startdate, enddate, dfcol, window1, window2):
        """
        It is using moving_average function to return two dataframes , one with smaller window and other with bigger one calculated in
        their 'ROLL' column.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param window1: int , bigger window (default 26)
        @param window2: int, smaller window (default 12)
        @return: t1, t2 both Dateframes with added column of 'ROLL' to them
        """
        t1 = MA.moving_average(df, startdate, enddate, dfcol, window1)
        t2 = MA.moving_average(df, startdate, enddate, dfcol, window2)
        return t1, t2

    def plotit(self, t1, t2):
        """
        Function for plotting bands in a time series graph.
        @param t1:
        @param t2:
        @return: void
        """
        plt.plot(t1['Date'], t1['roll'])
        plt.plot(t2['Date'], t2['roll'])

    def macdsig(self, df, startdate, enddate, dfcol, window1, window2):
        """
        Uses dataframe returned from macd func to get two moving averages then takes the difference of two.
        Diff will be positive or negative so we find where diff is changing signs and that will be our buy or sell signal.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param window1: int , bigger window (default 26)
        @param window2: int, smaller window (default 12)
        @return: Dataframe with 'SIGNAL' column added to it

        """
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
        """
        This function finds best performing window (n) and factor(m) by calculating profits while iterating over values of
        n and m in the range we have provided. It uses 'macdsig' function which in turn uses 'macd' function
        to generate signals and calculate profits for every value of n and m.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param dfcol: String, any price colunm on which to apply macd strategy on
        @param arr: arr is list of lists of the form [[startrange,endrange], [startrange,endrange]] where lists inside are in order
        of windowShort and windowLong , we could use this type of list too [step,+-range] but here for simplicity we assumed step
        is always integer 1 and hence we are not changing values by 0.1 or any other float number.

        @return: list ['maxprofit=', 'windowShort', 'windowLong=','MACD']

        """
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
