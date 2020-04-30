import numpy as np

from stock_trading.strategies.Main import Main


class Portfolio(Main):

    @classmethod
    def pfmanage(cls, df, dfcol):  # managing pf using first buy and sell signal
        Main.reset()
        if df.shape[0] == 0:
            return 0
        t2 = df.copy()
        t2 = t2[t2['signal'] != 'None']
        t2.reset_index(drop=True, inplace=True)
        if t2.shape[0] == 0:
            return 0
        # totalSellSig = str(t2[t2['signal'] == 'sell'].shape[0])
        # totalBuySig = str(t2[t2['signal'] == 'buy'].shape[0])
        # print("printing t2=================")
        # print(t2)
        t2['sigbinary'] = np.where(t2['signal'] == 'buy', 1, -1)
        # print("printing t2================= t2['sigbinary'] = np.where(t2['signal'] == 'buy', 1, -1)")
        # print(t2)
        t2['shifted'] = t2['sigbinary'].shift(1)
        # print("printing t2================= t2['shifted'] = t2['sigbinary'].shift(1)")
        # print(t2)
        t2['multi'] = t2['sigbinary'] * t2['shifted']
        # print("printing t2================= t2['multi'] = t2['sigbinary'] * t2['shifted']")
        # print(t2)
        t2['multi'].iloc[0] = -1
        # print("printing t2================= t2['multi'].iloc[0] = -1")
        # print(t2)
        t = t2[t2['multi'] == -1]
        # print("printing t,  t = t2[t2['multi'] == -1]")
        # print(t)
        mask = t['sigbinary'] == 1
        # print("mask, ")
        # print(mask)
        # print("printing exec of t")
        t['exec'] = np.where(mask, 'buy', 'sell')
        lastclose = float(t[-1:]['Close'])
        t = t.drop(columns=['shifted', 'multi', 'sigbinary'])
        if t['exec'].iloc[0] == 'buy':
            r = t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i] == 'buy':
                    Portfolio.updatepf(0, Main.money / t[dfcol].iloc[i], 'buy')
                if t['exec'].iloc[i] == 'sell':
                    Portfolio.updatepf(Main.stocks * t[dfcol].iloc[i], 0, 'sell')

        if t['exec'].iloc[0] == 'sell':
            t = t[1:]
            r = t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i] == 'buy':
                    Portfolio.updatepf(0, (Main.money * ((100 - Main.fee) / 100)) / t[dfcol].iloc[i], 'buy')
                if t['exec'].iloc[i] == 'sell':
                    Portfolio.updatepf(Main.stocks * t[dfcol].iloc[i], 0, 'sell')
        return Main.value(lastclose)
        # , totalBuySig, totalSellSig

    @classmethod
    def updatepf(cls, moneyvalue, stocksvalue, sig):
        if sig == 'sell':
            Main.money = moneyvalue * (100 - Main.fee) / 100  # if fee=1% then here I am returning (money*0.99)
            Main.stocks = stocksvalue
        if sig == 'buy':
            Main.stocks = stocksvalue
            Main.money = moneyvalue

    @classmethod
    def printpf(cls, t, i):
        print("Money and stocks are:  {}  ,{}   on date {} ".format(Main.money, Main.stocks, t['Date'].iloc[i]))
