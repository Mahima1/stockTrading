class Main:
    stocks = 0
    money = 10  # => Bitcoins are 10
    fee = 0.1

    @classmethod
    def value(cls, lastclose):
        if Main.money == 0:
            val = (Main.stocks * lastclose)
        elif Main.stocks == 0:
            val = Main.money
        else:
            val = "stocks or money not zero hence cannot calculate value"
        return val

    @classmethod
    def reset(cls):
        Main.stocks = 0
        Main.money = 10
