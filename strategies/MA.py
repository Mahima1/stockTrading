import matplotlib.pyplot as plt

from stock_trading.strategies.Strategy import Strategy


class MA(Strategy):
    """
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

    """
    Strategy.names.append('MA')

    def __init__(self):
        super(Strategy, self).__init__()

    @classmethod
    def moving_average(cls, df, start_date, end_date, dfcol, window):
        """
        @param df: Dataframe with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param start_date: Date ('YYYY-MM-DD')
        @param end_date: Date ('YYYY-MM-DD')
        @param dfcol: String, column of DataFrame whose moving average is to be calculated
        @param window: int
        @return: Dataframe with 'ROLL' column added into it which is the moving_average column

        """
        temp = Strategy.slicebydate(df, start_date, end_date)
        temp['roll'] = temp.rolling(window, min_periods=window)[dfcol].mean()
        return temp

    @classmethod
    def plotit(cls, temp):
        """
        Function for plotting bands in a time series graph.
        @param temp: Dataframe returned from moving_average func
        @return: void
        """
        plt.plot(temp['Date'], temp['roll'])

# -----------moving average function which was predicting next dates and applying rolling mean there too----------
# def moving_average(df,start_date,end_date,dfcol,window,days,minperiod=14):
#         import datetime
#         temp=Strategy.slicebydate(df,start_date,end_date)
#         # pd.date_range('2019-06-15 22:41:59.999000',periods=30,freq='60s')
#         # end_date,periods=days,freq='m'
#         temp2=pd.DataFrame()
#         temp2['Date']=pd.date_range(start=pd.to_datetime(1,origin=end_date,unit='D'),end=pd.to_datetime(days,origin=end_date,unit='D'))
#         temp=temp.append(temp2,ignore_index=True)
#         temp['roll']=temp.rolling(window, min_periods = minperiod)[dfcol].mean()
#         return temp


# -----------moving average function with minperiod default set and can be explicitely changed-------------------------
# def moving_average(df,start_date,end_date,dfcol,window,minperiod=14):
#         temp=Strategy.slicebydate(df,start_date,end_date)
#         temp['roll']=temp.rolling(window, min_periods = minperiod)[dfcol].mean()
#         return temp
