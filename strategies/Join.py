import pandas as pd

from stock_trading.strategies.Portfolio import Portfolio


class Join:
    """
    Usage:
    arr={'_boll':Boll.bolsig(df,'2017-07-14 05:30:00','2019-05-26 05:30:00',14),
         '_rsi':Rsi.rsisig(df, '2017-07-14 05:30:00','2019-05-26 05:30:00' ,70,20,'Close', 14),
         '_vol':Vol.volsig(df, '2017-07-14 05:30:00','2019-05-26 05:30:00' ,14)
        }

    join(arr)
    """

    def __init__(self):
        pass

    @classmethod
    def optimizer(cls, optmize_func_list):
        """
        This func takes
        @param optmize_func_list: list of optimizer functions for the strategies
        @return: var,  is list of the lists returned by various optimization functions
        """
        print("Running optimizer... ")
        count = len(optmize_func_list)
        profit = 0
        at_index = 0
        var = list()
        for i in range(count):
            p = optmize_func_list[i]
            p.append(i)
            var.append(p)
            # var.append(optmize_func_list[i])
            if profit < var[i][0]:
                profit = var[i][0]
            #     at_index = i
        # return var[at_index]
        return var

    @classmethod
    def join(cls, arr):
        joined = pd.DataFrame()
        list_of_keys = list(arr)
        first_key = list_of_keys[0]
        count = len(list_of_keys)
        joined = arr[first_key]
        joined = joined[joined['signal'] != 'None']
        if count == 1:
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
