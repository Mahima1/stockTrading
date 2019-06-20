import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np

from .Strategy import Strategy
from .MA import MA
from .Dr import Dr


class Vol(Strategy,MA):
    Strategy.names.append('Vol')

    def __init__(self):
        super(Strategy, self).__init__()
        super(MA, self).__init__()

    def volsig(df,startdate,enddate,window,days):
        temp=MA.moving_average2(df,startdate,enddate,'Volume',window,days)
        temp['%vol']=(abs(temp['Volume']-temp['roll'])/temp['roll'])*100
        temp['Close_dr']=((temp['Close'].shift(1)-temp['Close'])/temp['Close'])*100
        temp['signal']=np.where(temp['%vol']>=30, np.where(temp['Close_dr']>0,'buy','sell'), 'None')
#         return Strategy.profit2(temp)
        return temp
