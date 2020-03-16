import matplotlib.pyplot as plt
from .Strategy import Strategy


class MA:
    '''
Basic Info and Implementation:
A moving average (MA) is a widely used indicator in technical analysis that helps smooth out price action by
filtering out the “noise” from random short-term price fluctuations.
It is a trend-following, or lagging, indicator because it is based on past prices.
These moving averages are the simple moving average (SMA),
which is the simple average of a security over a defined number of time periods.

Implemented using 'rolling' function of pandas library

MA tell us:
Moving averages are a totally customizable indicator, which means that the user can freely choose whatever time
frame they want when creating the average. The most common time periods used in moving averages are 15, 20, 30, 50, 100, and 200 days.
The shorter the time span used to create the average, the more sensitive it will be to price changes.

Formulae:
SMA = (A1​ + A2​ + … + An​​) / n

where:
Ai = price of security for day i
n = number of time periods​

    '''
    Strategy.names.append('MA')

    def __init__(self, dfcol, window):
        super(Strategy, self).__init__()
        self.dfcol = dfcol
        self.window = window

    def moving_average(self, df, startdate, enddate, dfcol, window):
        '''
        @param df: Dataframe with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param window: int
        @param factor: int or float (default is set to 2)
        @return: Dataframe with 'ROLL' column added into it which is the moving_average column

        '''
        temp = Strategy.slicebydate(df, startdate, enddate)
        temp['roll'] = temp.rolling(window, min_periods=window)[dfcol].mean()
        return temp

    def plotit(self, temp):
        '''
        Function for plotting bands in a time series graph.
        @param temp: Dataframe returned from moving_average func
        @return: void
        '''
        plt.plot(temp['Date'], temp['roll'])

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
