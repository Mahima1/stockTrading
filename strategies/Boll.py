import matplotlib.pyplot as plt
import numpy as np
from .Portfolio import Portfolio
from .Strategy import Strategy
from .MA import MA


class Boll(Strategy, MA):
    '''
Basic Info and Implementation:
Bollinger Bands are a technical analysis tool.
There are three lines that compose Bollinger Bands: A simple moving average (middle band) and an upper and lower band.
The upper and lower bands are typically 2 standard deviations +/- from a 20-day simple moving average, but can be modified.

Bollinger Bands Tell us:
The closer the prices move to the upper band, the more overbought the market, hence a better chance of market moving towards equilibrium
i.e prices can go down and selling of stocks can be done before that happens.
The closer the prices move to the lower band, the more oversold the market

Formula:
BOLU= MA(TP,n) + (m∗σ[TP,n])
BOLD= MA(TP,n) − (m∗σ[TP,n])

where:
BOLU=Upper Bollinger Band
BOLD=Lower Bollinger Band
MA=Moving average
TP (typical price)=(High+Low+Close)÷3
n=Number of days in smoothing period (typically 20)
m=Number of standard deviations (typically 2)
σ[TP,n]=Standard Deviation over last n periods of TP
    '''

    Strategy.names.append('Bollinger_bands')

    # saved_args=0
    def __init__(self):
        super(Strategy, self).__init__()
        super(MA, self).__init__()

    def bollinger_bands(df, startdate, enddate, window, factor=2):
        '''
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param window: int
        @param factor: int or float (default is set to 2)
        @return: Dataframe with TYPICAL PRICE, STD (standard deviation), UPPER BAND, LOWER BAND columns added into it
        '''

        # Boll.saved_args=locals()
        temp = df.copy()
        temp['typical price'] = (temp['Close'] + temp['High'] + temp['Low']) / 3
        temp = MA.moving_average(temp, startdate, enddate, 'typical price', window)
        temp['std'] = temp.rolling(window, min_periods=window)['typical price'].std()
        temp['upper band'] = temp['roll'] + (factor * temp['std'])
        temp['lower band'] = temp['roll'] - (factor * temp['std'])
        return temp

    def plotit(temp):
        plt.plot(temp['Date'], temp['typical price'])
        plt.plot(temp['Date'], temp['upper band'])
        plt.plot(temp['Date'], temp['lower band'])

    def bolsig(df, startdate, enddate, window, factor=2):
        t = Boll.bollinger_bands(df, startdate, enddate, window, factor)
        mask1 = t['High'] >= t['upper band']
        mask = t['Low'] <= t['lower band']
        t['signal'] = np.where(mask, 'buy', (np.where(mask1, 'sell', 'None')))
        return t

    def boloptimize(df, startdate, enddate, arr):
        #         arr is list of lists of the form [[startrange,endrange], [startrange,endrange]] where lists inside are in order
        #         of window and factor , we could use this type of list too [step,+-range] but here for simplicity we assumed step
        #         is always integer 1 and hence we are not changing values by 0.1 or any other float number.
        maxprofit = factor = window = 0
        #     arr=[[10,80],[2,4]]          #use step here like [10,80,0.2] and inside inner loop chnage to window +=step
        count1 = arr[0][1] - arr[0][0] + 1
        count2 = arr[1][1] - arr[1][0] + 1
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
