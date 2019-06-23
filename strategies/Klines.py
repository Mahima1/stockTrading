import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline

from .Strategy import Strategy
from .MA import MA


class Klines(Strategy,MA):
    Strategy.names.append('Doji')
    Strategy.names.append('Umbrella')
    Strategy.names.append('Moribozu')

    def __init__(self):
        super(Strategy, self).__init__()
        super(MA, self).__init__()

    def doji(df,startdate,enddate,dfcol,window ):
        q1=MA.moving_average(df,startdate,enddate,dfcol,window )
        q3=q1.copy()
        q1['shiftedroll']=q1['roll'].shift(5)
        q3['slope']=(q1['roll']-q1['shiftedroll'])/5
        q3=q3[abs(q3['slope'])>=0.6]
        q3=q3[(abs((q1['High']-q1['Open'])/(q1['Close']-q1['Low'])))>=0.8]
        q3=q3[(abs((q1['High']-q1['Open'])/(q1['Close']-q1['Low'])))<=1.25]
        q3=q3[abs((q3['Open']-q3['Close'])/(q3['High']-q3['Low']))<=0.3]
        return q3
    #     print(q3)# if -ve denotes downward trend

    def umbrella(df,startdate,enddate,dfcol,window ):
        q1=MA.moving_average(df,startdate,enddate,dfcol,window )
        q3=q1.copy()
        q1['shiftedroll']=q1['roll'].shift(5)
        q3['slope']=(q1['roll']-q1['shiftedroll'])/5
        q3=q3[abs(q3['slope'])>=0.6]
        q3=q3[abs((q3['Open']-q3['Close'])/(q3['High']-q3['Low']))<=0.3]
        q3=q3[(abs((q1['Close']-q1['Low'])/(q1['High']-q1['Open'])))>=2]
        return q3

    def maribozu(df,startdate,enddate,dfcol,window ):
        temp=Strategy.slicebydate(df,startdate,enddate,dfcol,window )
        temp2=temp[abs((temp['Open']-temp['Close'])/(temp['High']-temp['Low']))>=0.95]
        return temp2


    def plotit(t,startdate,enddate):
        Strategy.candlesticks(t,startdate,enddate)
#
# Klines.doji(spy,'2007-08-08','2008-10-10')
# Klines.umbrella(spy,'2007-08-08','2008-10-10')
# Klines.maribozu(spy,'2007-08-08','2011-10-10')
