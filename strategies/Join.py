from .Portfolio import Portfolio


def optimizer(llist):
    count = len(llist)
    profit = 0
    at_index = 0
    var = list()
    for i in range(count):
        p = llist[i]
        p.append(i)
        var.append(p)
        # var.append(llist[i])         # var is list of lists returned by various optimize functions
        if profit < var[i][0]:
            profit = var[i][0]
            at_index = i
    # return var[at_index]
    return var


# optimizer(llist)

def join(arr):
    import pandas as pd

    joined = pd.DataFrame()
    list_of_keys = list(arr)
    first_key = list_of_keys[0]
    count = len(list_of_keys)
    joined = arr[first_key]
    joined = joined[joined['signal'] != 'None']
    if (count == 1):
        result = joined.dropna()
        temp = result.copy()
        temp.rename(columns={'signal' + first_key: 'signal'}, inplace=True)
        t = Portfolio.pfmanage(temp, 'Close')
        return t

    else:
        for i in range(1, count):
            q1 = arr[list_of_keys[i]]
            q1 = q1[['Date', 'signal']][q1['signal'] != 'None']
            first_key = list_of_keys[i - 1]
            joined = joined.join(q1.set_index('Date'), on='Date', how='outer', lsuffix=first_key,
                                 rsuffix=list_of_keys[i])
            joined['signal'] = 0
        result = joined.dropna()
        result = result.loc[:, ~result.columns.duplicated()]
        result = result.drop(columns=['signal'])
        result.rename(columns={'signal' + first_key: 'signal'}, inplace=True)
        t = Portfolio.pfmanage(result, 'Close')
        return t


from .Boll import Boll
from .Vol import Vol
from .Rsi import Rsi
from .Strategy import Strategy
from .MACD import MACD

# arr1=[[70,71],[20,21],[10,15]]
# arr2=[[10,12],[2,4]]
# llist=[
#        Rsi.rsioptimize(df,'2017-07-14 05:30:00','2019-05-26 05:30:00','Close',arr1),
#        Boll.boloptimize(df,'2017-07-14 05:30:00','2019-05-26 05:30:00',1,arr2)
#       ]

# arr={'_boll':Boll.bolsig(df,'2017-07-14 05:30:00','2019-05-26 05:30:00',14),
#      '_rsi':Rsi.rsisig(df, '2017-07-14 05:30:00','2019-05-26 05:30:00' ,70,20,'Close', 14),
#      '_vol':Vol.volsig(df, '2017-07-14 05:30:00','2019-05-26 05:30:00' ,14),
#      '_macd':MACD.macdsig(df,'2017-07-14 05:30:00','2019-05-26 05:30:00','Close',14,30)
#     }
# join(arr)
