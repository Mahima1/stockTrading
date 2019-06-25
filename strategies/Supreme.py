class Supreme:
    stocks=0
    money=10 #  =>Bitcoins are 10
    def value():
        if Supreme.money==0:
            val=Supreme.stocks
        elif Supreme.stocks==0:
            val=Supreme.money
        else:
            val=1
        return val
    def reset():
        Supreme.stocks=0
        Supreme.money=10


