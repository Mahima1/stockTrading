# -----------------MAOMA reperesents MOVING AVERAGE OF MOVING AVERAGE---------------------------

import matplotlib.pyplot as plt
import numpy as np

from stock_trading.strategies.MA import MA
from stock_trading.strategies.Portfolio import Portfolio
from stock_trading.strategies.Strategy import Strategy


class MAOMA(Strategy):
    """
    Basic Info and Implementation:
Moving Average Of Moving Average (MACD) is a trend-following momentum indicator
that shows the relationship between two moving averages of a security’s price.

The MAOMA is calculated by subtracting the 26-period Moving Average (MA) from the 12-period MA.

MAOMA tell us:
MAOMA triggers technical signals when it crosses above (to buy) or below (to sell) its signal line.
The speed of crossovers is also taken as a signal of a market is overbought or oversold.
The MACD has a positive value whenever the 12-period EMA (blue) is above the 26-period MA (red)
and a negative value when the 12-period MA is below the 26-period MA.

Formulae:
MACD = 12-Period MA − 26-Period MA

where:
MA is moving average
    """
    Strategy.names.append("Maoma")

    def __init__(self):
        super(Strategy, self).__init__()

    @classmethod
    def maoma(cls, df, start_date, end_date, dfcol, window1, window2):
        """
        MAOMA func creates two dataFrames with 'Roll' column added to them using moving_average func.
        t2 DataFrame has the moving_average of t1.

        @param df: Dataframe with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param start_date: Date ('YYYY-MM-DD')
        @param end_date: Date ('YYYY-MM-DD')
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param window1: int , bigger window (default 26)
        @param window2: int, smaller window (default 12)
        @return: t1, t2 both Dateframes with added column of 'ROLL' to them

        """
        t1 = MA.moving_average(df, start_date, end_date, dfcol, window1)
        t2 = MA.moving_average(t1, start_date, end_date, 'roll', window2)
        return t1, t2

    @classmethod
    def plotit(cls, t1, t2):
        """
        Function for plotting bands in a time series graph.
        @param t1: Dataframe returned from moving_average func
        @param t2: Dataframe returned from t1 whose MA is calculated
        @return: void
        """
        plt.plot(t1['Date'], t1['roll'])
        plt.plot(t2['Date'], t2['roll'])

    @classmethod
    def maomasig(cls, df, start_date, end_date, dfcol, window1, window2):
        """
        Uses dataframe returned from macd func to get two moving averages then takes the difference of two.
        Diff will be positive or negative so we find where diff is changing signs and that will be our buy or sell signal.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param start_date: Date ('YYYY-MM-DD')
        @param end_date: Date ('YYYY-MM-DD')
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param window1: int , bigger window (default 26)
        @param window2: int, smaller window (default 12)
        @return: Dataframe with 'SIGNAL' column added to it
        """
        q1, q2 = MAOMA.maoma(df, start_date, end_date, dfcol, window1, window2)
        q1['diff'] = q1['roll'] - q2['roll']
        q1['shift'] = (q1['diff'].shift(1))
        q1['multiple'] = q1['diff'] * q1['shift']
        mask = q1['multiple'] < 0
        mask1 = q1['shift'] > 0
        where1 = np.where(mask1, 'buy', 'sell')
        q1['signal'] = np.where(mask, where1, 'None')
        # lastSignal = q1[-1:]['signal']
        # return q1, lastSignal
        return q1

    @classmethod
    def maomaoptimize(cls, df, start_date, end_date, dfcol, arr):
        """
        This function finds best performing window (n) and factor(m) by calculating profits while iterating over values of
        n and m in the range we have provided. It uses 'macdsig' function which in turn uses 'macd' function
        to generate signals and calculate profits for every value of n and m.

        @param df: Dataframe with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param start_date: Date ('YYYY-MM-DD')
        @param end_date: Date ('YYYY-MM-DD')
        @param dfcol: String, any price colunm on which to apply maoma strategy on
        @param arr: arr is list of lists of the form [[startrange,endrange], [startrange,endrange]] where lists inside are in order
        of windowShort and windowLong , we could use this type of list too [step,+-range] but here for simplicity we assumed step
        is always integer 1 and hence we are not changing values by 0.1 or any other float number.

        @return: list ['maxprofit=', 'windowShort', 'windowLong=','MAOMA']

        """
        maxprofit = windowshort = windowlong = 0
        count1 = arr[0][1] - arr[0][0] + 1
        count2 = arr[1][1] - arr[1][0] + 1
        w1 = arr[0][0]
        for p in range(count1):
            w2 = arr[1][0]
            for e in range(count2):
                t = MAOMA.maomasig(df, start_date, end_date, dfcol, w1, w2)
                net = Portfolio.pf_manage(t, 'Close')
                if maxprofit < net:
                    maxprofit = net
                    windowshort = w1
                    windowlong = w2
                w2 += 1
            w1 += 1
        return [maxprofit, windowshort, windowlong, 'MAOMA']
