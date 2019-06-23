import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline

from .Strategy import Strategy


class MA:
    Strategy.names.append('MA')

    def __init__(self,dfcol,window,days):
        super(Strategy, self).__init__()
        self.dfcol=dfcol
        self.window=window
        self.days=days

    def moving_average(df,startdate,enddate,dfcol,window,days,minperiod=14):
            import datetime
            temp=Strategy.slicebydate2(df,startdate,enddate)
            temp2=pd.DataFrame()
            # timedelta=pd.to_timedelta()
            # pd.date_range('2019-06-15 22:41:59.999000',periods=30,freq='60s')
            # enddate,periods=days,freq='m'
            temp2['Date']=pd.date_range(start=pd.to_datetime(1,origin=enddate,unit='D'),end=pd.to_datetime(days,origin=enddate,unit='D'))
            temp=temp.append(temp2,ignore_index=True)
            temp['roll']=temp.rolling(window, min_periods = minperiod)[dfcol].mean()
            return temp
        #     plt.plot(temp['Date'],temp['roll'])
