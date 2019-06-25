class Main:
    stocks=0
    money=10 #  =>Bitcoins are 10
    
    def value(lastclose):
        if Main.money==0:
            val=Main.stocks*lastclose
        elif Main.stocks==0:
            val=Main.money
        else:
            val="stocks or money not zero hence cannot calculate value"
        return val
    def reset():
        Main.stocks=0
        Main.money=10


