import numpy as np
import pandas as pd
from .Supreme import Supreme


class Portfolio(Supreme):
    def pfmanage(df,dfcol): #managing pf using first buy and sell signal
        Supreme.reset()
        t2=df.copy()
        t2['sigbinary']=np.where(t2['signal']=='buy',1,np.where(t2['signal']=='sell',-1,0))
        t2['shifted']=t2['sigbinary'].shift(1)
        t2['multi']=t2['sigbinary']*t2['shifted']
        t2['multi'].iloc[0]=-1
        t=t2[t2['multi']==-1]
        mask=t['sigbinary']==1
        t['exec']=np.where(mask,'buy','sell')
        t=t.drop(columns=['shifted','multi','sigbinary'])
        # Portfolio.printpf(t,0)
        if t['exec'].iloc[0]=='buy':
            r=t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i]=='buy':
                    Portfolio.updatepf(0,Supreme.money/t[dfcol].iloc[i],'buy')
                    # Portfolio.printpf(t,i)
                if t['exec'].iloc[i]=='sell':
                    Portfolio.updatepf(Supreme.stocks*t[dfcol].iloc[i],0,'sell')
                    # Portfolio.printpf(t,i)

        if t['exec'].iloc[0]=='sell':
            t=t[1:]
            r=t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i]=='buy':
                    Portfolio.updatepf(0,Supreme.money/t[dfcol].iloc[i],'buy')
                    # Portfolio.printpf(t,i)
                if t['exec'].iloc[i]=='sell':
                    Portfolio.updatepf(Supreme.stocks*t[dfcol].iloc[i],0,'sell')
                    # Portfolio.printpf(t,i)
        # return Supreme.value()
        return t
    def updatepf(moneyvalue,stocksvalue,sig):
        if sig=='sell':
            Supreme.money=moneyvalue
            Supreme.stocks=stocksvalue
        if sig=='buy':
            Supreme.stocks=stocksvalue
            Supreme.money=moneyvalue

        
    def printpf(t,i):
        print("Money and stocks are:  {}  ,{}   on date {} ".format(Supreme.money,Supreme.stocks,t['Date'].iloc[i]))

