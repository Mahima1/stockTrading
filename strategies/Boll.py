import matplotlib.pyplot as plt
import numpy as np

from .MA import MA
from .Portfolio import Portfolio
from .Strategy import Strategy


class Boll(Strategy, MA):
    """
Basic Info and Implementation:
Bollinger Bands are a technical analysis tool.
There are three lines that compose Bollinger Bands: A simple moving average (middle band) and an upper and lower band.
The upper and lower bands are typically 2 standard deviations +/- from a 20-day simple moving average, but can be modified.

Bollinger Bands Tell us:
The closer the prices move to the upper band, the more overbought the market, hence a better chance of market moving towards equilibrium
i.e prices can go down and selling of stocks can be done before that happens.
The closer the prices move to the lower band, the more oversold the market

Formula:
Upper Band = MA(TP,n) + (m∗σ[TP,n])
Lower Band = MA(TP,n) − (m∗σ[TP,n])

where:
Upper Band = Upper Bollinger Band
Lower Band = Lower Bollinger Band
MA=Moving average
TP (typical price)=(High+Low+Close)/3
n=Number of days in smoothing period (typically 20)
m=Number of standard deviations (typically 2)
σ[TP,n]=Standard Deviation over last n periods of TP
    """

    Strategy.names.append('Bollinger_bands')

    # saved_args=0
    def __init__(self):
        super(Strategy, self).__init__()
        super(MA, self).__init__()

    @classmethod
    def bollinger_bands(cls, df, startdate, enddate, window, factor=2):
        """
        Calculates moving_average of TP ( typical price ) and its std deviation then upper band (+factor*std deviation)
        and lower band  (-factor*std deviation) wrt moving_average line.

        @param df: Dataframe with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param window: int
        @param factor: int or float (default is set to 2)
        @return: Dataframe with TYPICAL PRICE, STD (standard deviation), UPPER BAND, LOWER BAND columns added into it
        """

        # Boll.saved_args=locals()
        temp = df.copy()
        temp['typical price'] = (temp['Close'] + temp['High'] + temp['Low']) / 3
        temp = MA.moving_average(temp, startdate, enddate, 'typical price', window)
        temp['std'] = temp.rolling(window, min_periods=window)['typical price'].std()
        temp['upper band'] = temp['roll'] + (factor * temp['std'])
        temp['lower band'] = temp['roll'] - (factor * temp['std'])
        return temp

    @classmethod
    def plotit(cls, temp):
        """
        Function for plotting bands in a time series graph.
        @param temp: Dataframe returned from Bollinger_bands function.
        @return: void
        """

        plt.plot(temp['Date'], temp['typical price'])
        plt.plot(temp['Date'], temp['upper band'])
        plt.plot(temp['Date'], temp['lower band'])

    def bolsig(self, df, startdate, enddate, window, factor=2):
        """
        Uses dataframe returned from bollingerbands func to get upper rand lower bands then we compare 'High' and 'Low'
        with those bands and generate signal of sell as high surpasses upper and low declines below lower.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param window: int
        @param factor: int or float (default = 2)
        @return: Dataframe with 'SIGNAL' column added to it
        """
        t = Boll.bollinger_bands(df, startdate, enddate, window, factor)
        mask1 = t['High'] >= t['upper band']
        mask = t['Low'] <= t['lower band']
        t['signal'] = np.where(mask, 'buy', (np.where(mask1, 'sell', 'None')))
        return t

    def boloptimize(self, df, startdate, enddate, arr):
        """
        This function finds best performing window (n) and factor(m) by calculating profits while iterating over values of
        n and m in the range we have provided. It uses 'Bolsig' function which in turn uses 'bollinger_bands' function
        to generate signals and calculate profits for every value of n and m.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param arr: arr is list of lists of the form [[startrange,endrange], [startrange,endrange]] where lists inside are in order
        of window and factor , we could use this type of list too [step,+-range] but here for simplicity we assumed step
        is always integer 1 and hence we are not changing values by 0.1 or any other float number.

        @return: list ['maxprofit=', 'window=', 'factor=','Boll']
        """

        maxprofit = factor = window = 0
        #     arr=[[10,80],[2,4]]          #use step here like [10,80,0.2] and inside inner loop change to window +=step
        count1 = arr[0][1] - arr[0][0] + 1
        # count for outer loop iterating over range of window
        count2 = arr[1][1] - arr[1][0] + 1
        # count for inner loop iterating over multiple of sigma
        w = arr[0][0]
        for p in range(count1):
            f = arr[1][0]
            for e in range(count2):
                t = Boll.bolsig(df, startdate, enddate, w, f)
                net = Portfolio.pfmanage(t, 'Close')
                if maxprofit < net:
                    maxprofit = net
                    factor = f
                    window = w
                f += 1
            w += 1
        return [maxprofit, window, factor, 'Boll']
