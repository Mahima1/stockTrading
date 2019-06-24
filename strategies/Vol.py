import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

import numpy as np
from .Strategy import Strategy
from .Portfolio import Portfolio
from .MA import MA


class Vol(Strategy,MA,Portfolio):
    Strategy.names.append('Vol')

    def __init__(self):
        super(Strategy, self).__init__()
        super(MA, self).__init__()

    def volsig(df,startdate,enddate,window):
        temp=MA.moving_average(df,startdate,enddate,'Volume',window)
        temp['%vol']=(abs(temp['Volume']-temp['roll'])/temp['roll'])*100
        temp['Close_dr']=((temp['Close'].shift(1)-temp['Close'])/temp['Close'])*100
        temp['signal']=np.where(temp['%vol']>=30, np.where(temp['Close_dr']>0,'buy','sell'), 'None')
#         return Strategy.profit(temp)
        return temp

    def voloptimize(df,startdate,enddate,arr):
        maxprofit=window=0
        count1=arr[0][1]-arr[0][0]+1
        #we could have passed single list too like arr=[5,100]
        w=arr[0][0]
        for p in range(count1):
            t=Vol.volsig(df,startdate,enddate,w)
            net=Portfolio.pfmanage(t,'Close')
            if maxprofit<net:
                maxprofit=net
                window=w
            w+=1
        return [maxprofit,window,'Vol'] #,rrr[['Date','sigvol','Close','signal']]



# arr=[[5,80]]
# voloptimize(df,'2017-07-14 05:30:00','2019-05-26 05:30:00',1,arr)
