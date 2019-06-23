# from .Strategy import Strategy
# from .Supreme import Supreme
#
# class Portfolio(Strategy,Supreme):
# def profit(df,dfcol):
#         df['sigvol'] =  np.where((df['signal']!='None'), (Supreme.money/df[dfcol]) , 0)
#         df['bought']=np.where(df['signal']=='buy' , df['sigvol']*df[dfcol] , 0)
#         df['sold']=np.where(df['signal']=='sell' , df['sigvol']*df[dfcol] , 0)
#         net=df['sold'].sum()-df['bought'].sum()
#         return net

    # def pfmanage(df):
    #     df['signal']=='buy'
class Portfolio(Supreme):
    import numpy as np
    def pfmanage(df,dfcol): #managing pf using first buy and sell signal
        t2=df.copy()
        t2['sigbinary']=np.where(t2['signal']=='buy',1,-1)
        t2['shift']=t2['sigbinary'].shift(1)
        t2['mult']=t2['sigbinary']*t2['shift']
        t2['mult'].iloc[0]=-1
        mask1=t2['mult']==-1
        t=t2[mask1]
        mask2=t['sigbinary']==1
        t['exec']=np.where(mask2,'buy','sell')
        print("Initially Money and stocks are:  {}  ,{}   on date {} ".format(Supreme.money,Supreme.stocks,t['Date'].iloc[0]))
        if t['exec'].iloc[0]=='buy':
            r=t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i]=='buy':
                    Supreme.stocks=Supreme.money/t[dfcol].iloc[i]
                    Supreme.money=0
                    print("Money and stocks are:  {}  ,{}   on date {} ".format(Supreme.money,Supreme.stocks,t['Date'].iloc[i]))
                if t['exec'].iloc[i]=='sell':
                    Supreme.money=Supreme.stocks*t[dfcol].iloc[i]
                    Supreme.stocks=0
                    print("Money and stocks are:  {}  ,{}   on date {} ".format(Supreme.money,Supreme.stocks,t['Date'].iloc[i]))

        if t['exec'].iloc[0]=='sell':
            t=t[1:]
            r=t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i]=='buy':
                    Supreme.stocks=Supreme.money/t[dfcol].iloc[i]
                    Supreme.money=0
                    print("Money and stocks are:  {}  ,{}   on date {} ".format(Supreme.money,Supreme.stocks,t['Date'].iloc[i]))
                if t['exec'].iloc[i]=='sell':
                    Supreme.money=Supreme.stocks*t[dfcol].iloc[i]
                    Supreme.stocks=0
                    print("Money and stocks are:  {}  ,{}   on date {} ".format(Supreme.money,Supreme.stocks,t['Date'].iloc[i]))

arr={'Boll':Boll.bolsig(df,'2017-07-14 05:30:00','2019-05-26 05:30:00',14,1 ),
     'Rsi':Rsi.rsisig(df, '2017-07-14 05:30:00','2019-05-26 05:30:00' ,70,20,'Close', 14)}

Portfolio.pfmanage(arr)

