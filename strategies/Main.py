class Main:
    stocks=0
    money=10 #  =>Bitcoins are 10
    
    def value():
        if Main.money==0:
            val=Main.stocks
        elif Main.stocks==0:
            val=Main.money
        else:
            val=1
        return val
    def reset():
        Main.stocks=0
        Main.money=10


