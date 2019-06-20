import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

import numpy as np

from .Strategy import Strategy

class Rsi(Strategy):
    Strategy.names.append('Rsi')

    def __init__(self,dfcol,window):
        super(Strategy, self).__init__()
        super(Strategy, self).__init__()
        self.dfcol=dfcol
        self.window=window

    def rsi(df,startdate,enddate,dfcol,window):
        temp=Strategy.slicebydate2(df,startdate,enddate)
        temp2=temp[dfcol].diff()
        profit, loss = temp2.copy(), temp2.copy()
        profit[profit < 0] = 0
        loss[loss > 0] = 0
        profitroll=profit.rolling(window, min_periods = 1).mean()
        lossroll=loss.rolling(window, min_periods = 1).mean().abs()
        x=profitroll/lossroll
        x=(x/(1+x))
        temp['rsi']=(x*100)
        return temp
#         temp.plot(x='Date',y='rsi')

    def rsisig(df,startdate,enddate,upperlimit,lowerlimit,dfcol,window):
        t=Rsi.rsi(df,startdate,enddate,dfcol,window)
        mask = t['rsi']<=lowerlimit
        mask1=t['rsi']>=upperlimit
        t['signal'] = np.where(mask,'buy',(np.where(mask1,'sell','None')))
    #     print (t[['Date','rsi']][t['signal']=='sell'])
    #     return Strategy.profit2(t)
    #     print("Profit is: ",net)
        return t


# Rsi.rsi(apple,'2008-01-01','2008-10-10','Adj Close',30)
