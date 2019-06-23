# -----------moving average function which was predicting next dates and applying rolling mean there too----------
# def moving_average(df,startdate,enddate,dfcol,window,days,minperiod=14):
    #         import datetime
    #         temp=Strategy.slicebydate(df,startdate,enddate)
    #         # pd.date_range('2019-06-15 22:41:59.999000',periods=30,freq='60s')
    #         # enddate,periods=days,freq='m'
    #         temp2=pd.DataFrame()
    #         temp2['Date']=pd.date_range(start=pd.to_datetime(1,origin=enddate,unit='D'),end=pd.to_datetime(days,origin=enddate,unit='D'))
    #         temp=temp.append(temp2,ignore_index=True)
    #         temp['roll']=temp.rolling(window, min_periods = minperiod)[dfcol].mean()
    #         return temp



# -----------moving average function with minperiod default set and can be explicitely changed-------------------------
# def moving_average(df,startdate,enddate,dfcol,window,minperiod=14):
#         temp=Strategy.slicebydate(df,startdate,enddate)
#         temp['roll']=temp.rolling(window, min_periods = minperiod)[dfcol].mean()
#         return temp



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline

from .Strategy import Strategy


class MA:
    Strategy.names.append('MA')

    def __init__(self,dfcol,window):
        super(Strategy, self).__init__()
        self.dfcol=dfcol
        self.window=window


    def moving_average(df,startdate,enddate,dfcol,window):
        temp=Strategy.slicebydate(df,startdate,enddate)
        temp['roll']=temp.rolling(window, min_periods = window)[dfcol].mean()
        return temp

    def plotit(temp):
        plt.plot(temp['Date'],temp['roll'])


