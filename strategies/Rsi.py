import numpy as np
from .Portfolio import Portfolio
from .Strategy import Strategy


class Rsi(Strategy):
    Strategy.names.append('Rsi')

    def __init__(self, dfcol, window):
        super(Strategy, self).__init__()
        super(Strategy, self).__init__()
        self.dfcol = dfcol
        self.window = window

    def rsi(df, startdate, enddate, dfcol, window):
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

    def plotit(temp):
        temp.plot(x='Date', y='rsi')

    def rsisig(df, startdate, enddate, upperlimit, lowerlimit, dfcol, window):
        t = Rsi.rsi(df, startdate, enddate, dfcol, window)
        mask = t['rsi'] <= lowerlimit
        mask1 = t['rsi'] >= upperlimit
        t['signal'] = np.where(mask, 'buy', (np.where(mask1, 'sell', 'None')))
        return t

    def rsioptimize(df, startdate, enddate, dfcol, arr):
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
