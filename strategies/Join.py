from .Boll import Boll
from .Vol import Vol
from .Rsi import Rsi
from .Strategy import Strategy
from .MACD import MACD
from .Portfolio import Portfolio



# arr1=[[70,71],[20,21],[10,15]]
# arr2=[[10,12],[2,4]]
# llist=[
#        Rsi.rsioptimize(df,'2017-07-14 05:30:00','2019-05-26 05:30:00','Close',arr1),
#        Boll.boloptimize(df,'2017-07-14 05:30:00','2019-05-26 05:30:00',1,arr2)
#       ]

def optimizer(llist):
    count=len(llist)
    profit=0
    at_index=0
    var=list()
    for i in range(count):
        var.append(llist[i])         # var is list of lists returned by various optimize functions
        if profit<var[i][0]:
            profit=var[i][0]
            at_index=i
    return var[at_index]

# optimizer(llist)

def join(arr):

    from .Boll import Boll
    from .Vol import Vol
    from .Rsi import Rsi
    from .Strategy import Strategy
    from .MACD import MACD
    import pandas as pd

    joined=pd.DataFrame()
    list_of_keys=list(arr)
    first_key=list_of_keys[0]
    count=len(list_of_keys)
    net=0

    joined=arr[first_key]
    joined=joined[joined['signal']!='None']
    if (count==1):
        result=joined.dropna()
        temp=result.copy()
        temp.rename(columns={'signal'+first_key:'signal'}, inplace=True)
        Portfolio.pfmanage(temp,'Close')
        # net=Strategy.profit(temp,'Close')
        # print ("Net profit is: {} ".format(net))
        # return result

    else:
        for i in range(1,count):
            q1=arr[list_of_keys[i]]
            q1=q1[['Date','signal']][q1['signal']!='None']
            first_key=list_of_keys[i-1]
            joined=joined.join(q1.set_index('Date'),on='Date',how='outer',lsuffix=first_key,rsuffix=list_of_keys[i])
            result=joined.dropna()
            temp=result.copy()
            temp.rename(columns={'signal'+first_key:'signal'}, inplace=True)
            Portfolio.pfmanage(temp,'Close')
        # net=Strategy.profit(temp,'Close')
        # print ("Net profit is: {} ".format(net))
        # return temp



# arr={'Boll':Boll.bolsig(df,'2017-07-14 05:30:00','2019-05-26 05:30:00',14,1 ),
#      'Rsi':Rsi.rsisig(df, '2017-07-14 05:30:00','2019-05-26 05:30:00' ,70,20,'Open', 14)}
# join(arr)
