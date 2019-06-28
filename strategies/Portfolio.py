import numpy as np
from .Main import Main


class Portfolio(Main):
    def pfmanage(df,dfcol): # managing pf using first buy and sell signal
        Main.reset()
        if df.shape[0]==0:
            return 0
        t2=df.copy()
        t2=t2[t2['signal']!='None']
        t2['sigbinary']=np.where(t2['signal']=='buy',1,-1)
        t2['shifted']=t2['sigbinary'].shift(1)
        t2['multi']=t2['sigbinary']*t2['shifted']
        # return t2
        # print ("shape is: ",t2.shape)
        t2['multi'].iloc[0]=-1
        t=t2[t2['multi']==-1]
        mask=t['sigbinary']==1
        t['exec']=np.where(mask,'buy','sell')
        lastclose=float(t[-1:]['Close'])
        t=t.drop(columns=['shifted','multi','sigbinary'])
        # Portfolio.printpf(t,0)
        if t['exec'].iloc[0]=='buy':
            # print("inside first buy signal df\n")
            r=t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i]=='buy':
                    Portfolio.updatepf(0,Main.money/t[dfcol].iloc[i],'buy')
                    # Portfolio.printpf(t,i)
                if t['exec'].iloc[i]=='sell':
                    Portfolio.updatepf(Main.stocks*t[dfcol].iloc[i],0,'sell')
                    # Portfolio.printpf(t,i)

        if t['exec'].iloc[0]=='sell':
            # print("inside first buy signal df")
            t=t[1:]
            r=t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i]=='buy':
                    Portfolio.updatepf(0,Main.money/t[dfcol].iloc[i],'buy')
                    # Portfolio.printpf(t,i)
                if t['exec'].iloc[i]=='sell':
                    Portfolio.updatepf(Main.stocks*t[dfcol].iloc[i],0,'sell')
                    # Portfolio.printpf(t,i)
        return Main.value(lastclose)
        # return t
    def updatepf(moneyvalue,stocksvalue,sig):
        if sig=='sell':
            Main.money=moneyvalue
            Main.stocks=stocksvalue
        if sig=='buy':
            Main.stocks=stocksvalue
            Main.money=moneyvalue

        
    def printpf(t,i):
        print("Money and stocks are:  {}  ,{}   on date {} ".format(Main.money,Main.stocks,t['Date'].iloc[i]))

