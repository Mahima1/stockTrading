import numpy as np

from stock_trading.strategies.MA import MA
from stock_trading.strategies.Portfolio import Portfolio
from stock_trading.strategies.Strategy import Strategy


class Vol(Strategy):
    Strategy.names.append('Vol')

    def __init__(self):
        super(Strategy, self).__init__()

    @classmethod
    def volsig(cls, df, start_date, end_date, window):
        temp = MA.moving_average(df, start_date, end_date, 'Volume', window)
        temp['%vol'] = (abs(temp['Volume'] - temp['roll']) / temp['roll']) * 100
        temp['Close_dr'] = ((temp['Close'].shift(1) - temp['Close']) / temp['Close']) * 100
        temp['signal'] = np.where(temp['%vol'] >= 30, np.where(temp['Close_dr'] > 0, 'buy', 'sell'), 'None')
        #         return Strategy.profit(temp)
        return temp

    @classmethod
    def voloptimize(cls, df, start_date, end_date, arr):
        maxprofit = window = 0
        count1 = arr[0][1] - arr[0][0] + 1
        # we could have passed single list too like arr=[5,100]
        w = arr[0][0]
        for p in range(count1):
            t = Vol.volsig(df, start_date, end_date, w)
            net = Portfolio.pfmanage(t, 'Close')
            if maxprofit < net:
                maxprofit = net
                window = w
            w += 1
        return [maxprofit, window, 'Vol']  # ,rrr[['Date','sigvol','Close','signal']]
