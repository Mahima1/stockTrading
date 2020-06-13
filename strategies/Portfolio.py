import numpy as np
from stock_trading.strategies.Main import Main


class Portfolio(Main):

    @classmethod
    def pf_manage(cls, df, dfcol):  # managing pf using first buy and sell signal
        previous_money_value = Main.pf_value
        Main.reset()
        if df.shape[0] == 0:
            return 0
        t2 = df.copy()
        t2 = t2[t2['signal'] != 'None']
        t2.reset_index(drop=True, inplace=True)
        if t2.shape[0] == 0:
            return 0

        t2['sigbinary'] = np.where(t2['signal'] == 'buy', 1, -1)
        t2['shifted'] = t2['sigbinary'].shift(1)
        t2['multi'] = t2['sigbinary'] * t2['shifted']
        t2['multi'].iloc[0] = -1
        t = t2[t2['multi'] == -1]
        mask = t['sigbinary'] == 1
        t['exec'] = np.where(mask, 'buy', 'sell')
        lastclose = float(t[-1:]['Close'])

        t = t.drop(columns=['shifted', 'multi', 'sigbinary'])
        if t['exec'].iloc[0] == 'buy':
            r = t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i] == 'buy':
                    Portfolio.update_pf(0, Main.money / t[dfcol].iloc[i], 'buy')
                if t['exec'].iloc[i] == 'sell':
                    Portfolio.update_pf(Main.stocks * t[dfcol].iloc[i], 0, 'sell')

        if t['exec'].iloc[0] == 'sell':
            t = t[1:]
            r = t.shape[0]
            for i in range(r):
                if t['exec'].iloc[i] == 'buy':
                    Portfolio.update_pf(0, (Main.money * ((100 - Main.fee) / 100)) / t[dfcol].iloc[i], 'buy')
                if t['exec'].iloc[i] == 'sell':
                    Portfolio.update_pf(Main.stocks * t[dfcol].iloc[i], 0, 'sell')

        last_pf_value = Main.pf_value
        current_money_value = Main.value(lastclose)
        dr = ((current_money_value - last_pf_value) / last_pf_value) * 100
        print("observed dr is: " + "{:.1f}".format(dr))
        return current_money_value

    @classmethod
    def update_pf(cls, money_value, stocks_value, sig):
        """

        @param money_value:
        @param stocks_value:
        @param sig:
        @return:
        """
        if sig == 'sell':
            Main.money = money_value * (100 - Main.fee) / 100  # if fee=1% then here I am returning (money*0.99)
            Main.stocks = stocks_value
        if sig == 'buy':
            Main.stocks = stocks_value
            Main.money = money_value

    @classmethod
    def print_pf(cls, t, i):
        print("Money and stocks are:  {}  ,{}   on date {} ".format(Main.money, Main.stocks, t['Date'].iloc[i]))
