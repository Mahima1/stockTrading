import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline

from .Strategy import Strategy
from .MA import MA


class Boll(Strategy,MA):
    Strategy.names.append('Bollinger_bands')

    def __init__(self):
        super(Strategy, self).__init__()
        super(MA, self).__init__()

    def bollinger_bands(df,startdate,enddate,window,days):
        temp=df
        temp['typical price']=(temp['Close']+temp['High']+temp['Low'])/3
        temp=MA.moving_average2(temp,startdate,enddate,'typical price',window,days)
        temp['std']=temp.rolling(window, min_periods = 1)['typical price'].std()
        temp['upper band']=temp['roll']+(3*temp['std'])
        temp['lower band']=temp['roll']-(3*temp['std'])
        return temp
#         plt.plot(temp['Date'],temp['typical price'])
#         plt.plot(temp['Date'],temp['upper band'])
#         plt.plot(temp['Date'],temp['lower band'])

    def bolsig(df,startdate,enddate,window,days):
        t=Boll.bollinger_bands(df,startdate,enddate,window,days)
        mask1=t['High']>=t['upper band']
        mask=t['Low']<=t['lower band']
        t['signal'] = np.where(mask,'buy',(np.where(mask1,'sell','None')))
        # return Strategy.profit2(t)
        return t

# Boll.bollinger_bands(spy,'2008-01-01','2008-10-10',15,1)
