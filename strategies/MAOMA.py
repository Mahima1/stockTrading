import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

from .Strategy import Strategy
from .MA import MA
   

class MAOMA(Strategy,MA):
    Strategy.names.append("Maoma")

    def __init__(self,window1,window2):
        super(Strategy, self).__init__()
        super(MA, self).__init__()
        self.window1=window1
        self.window2=window2

    def maoma(df,startdate,enddate,dfcol,window1,window2,days,):
        t1=MA.moving_average2(df,startdate,enddate,dfcol,window1,days,)
        t2=MA.moving_average2(t1,startdate,enddate,'roll',window2,days,)
    #     plt.plot(t1['Date'],t1['roll'])
    #     plt.plot(t2['Date'],t2['roll'])
        return t1,t2
# MAOMA.maoma(spy,'2007-08-08','2008-12-12','Adj Close',15,15,1)
