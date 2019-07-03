# -----------------MAOMA reperesents MOVING AVERAGE OF MOVING AVERAGE---------------------------

import matplotlib.pyplot as plt
from .Strategy import Strategy
from .MA import MA
from .Portfolio import Portfolio
import numpy as np


class MAOMA(Strategy, MA):
    Strategy.names.append("Maoma")

    def __init__(self, window1, window2):
        super(Strategy, self).__init__()
        super(MA, self).__init__()
        self.window1 = window1
        self.window2 = window2

    def maoma(df, startdate, enddate, dfcol, window1, window2):
        t1 = MA.moving_average(df, startdate, enddate, dfcol, window1)
        t2 = MA.moving_average(t1, startdate, enddate, 'roll', window2)
        return t1, t2

    def plotit(t1, t2):
        plt.plot(t1['Date'], t1['roll'])
        plt.plot(t2['Date'], t2['roll'])

    def maomasig(df, startdate, enddate, dfcol, window1, window2):
        q1, q2 = MAOMA.maoma(df, startdate, enddate, dfcol, window1, window2)
        q1['diff'] = q1['roll'] - q2['roll']
        q1['shift'] = (q1['diff'].shift(1))
        q1['multiple'] = q1['diff'] * q1['shift']
        mask = q1['multiple'] < 0
        mask1 = q1['shift'] > 0
        where1 = np.where(mask1, 'buy', 'sell')
        q1['signal'] = np.where(mask, where1, 'None')
        return q1
        # if q1.shape[0]==0:
        #     return 0
        # else:
        #     return q1

    def maomaoptimize(df, startdate, enddate, dfcol, arr):
        maxprofit = windowshort = windowlong = 0
        count1 = arr[0][1] - arr[0][0] + 1
        count2 = arr[1][1] - arr[1][0] + 1
        w1 = arr[0][0]
        for p in range(count1):
            w2 = arr[1][0]
            for e in range(count2):
                t = MAOMA.maomasig(df, startdate, enddate, dfcol, w1, w2)
                # net=Strategy.profit(t,'Close')
                net = Portfolio.pfmanage(t, 'Close')
                if maxprofit < net:
                    maxprofit = net
                    windowshort = w1
                    windowlong = w2
                w2 += 1
            w1 += 1
        return [maxprofit, windowshort, windowlong, 'MAOMA']

# arr=[[5,30],[60,80]]
# maomaoptimize(df,'2017-07-14 05:30:00','2019-05-26 05:30:00','Close',arr)

# maoma(spy,'2007-08-08','2008-12-12','Adj Close',15,100,10)


# MAOMA.maoma(spy,'2007-08-08','2008-12-12','Adj Close',15,15,1)
