import pandas as pd


class Main:
    stocks = 0
    money = 10  # => Bitcoins are 10
    fee = 0.1
    pf_value = 10  # it is money if money !=0 else it is money value of stocks

    # pf_value_df = pd.DataFrame(columns=['Date', 'value'])

    @classmethod
    def value(cls, last_close):
        if Main.money == 0:
            Main.pf_value = (Main.stocks * last_close)
        elif Main.stocks == 0:
            Main.pf_value = Main.money
        else:
            Main.pf_value = "stocks or money not zero hence cannot calculate value"
        return Main.pf_value

    @classmethod
    def reset(cls):
        Main.stocks = 0
        Main.money = 10
        Main.pf_value = 10
        # Main.pf_value_df = Main.pf_value_df.iloc[0:0]
