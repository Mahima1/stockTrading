import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline

from .Strategy import Strategy
from .MA import MA


class MACD(Strategy,MA):
    Strategy.names.append('MACD')

    def __init__(self,window1,window2):
        super(Strategy, self).__init__()
        super(MA, self).__init__()
        self.window1=window1
        self.window2=window2

    def macd(df,startdate,enddate,dfcol,window1,window2,days):
        t1=MA.moving_average2(df,startdate,enddate,dfcol,window1,days)
        t2=MA.moving_average2(df,startdate,enddate,dfcol,window2,days)
        # plt.plot(t1['Date'],t1['roll'])
        # plt.plot(t2['Date'],t2['roll'])
        return t1,t2

    def macdsig(df,startdate,enddate,dfcol,window1,window2,days):
        q1,q2=MACD.macd(df,startdate,enddate,dfcol,window1,window2,days)
        q1['diff']=q1['roll']-q2['roll']
        q1['shift']=(q1['diff'].shift(1))
        q1['multiple']=q1['diff']*q1['shift']
        mask = q1['multiple']<0
        mask1=q1['shift']>0
        where1=np.where(mask1,'buy','sell')
        q1['signal'] = np.where(mask,where1,'None')
        return q1

# macd(spy,'2007-08-08','2008-12-12','Adj Close',15,100,10)
