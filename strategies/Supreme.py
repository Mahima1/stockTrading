class Supreme:
    stocks=0
    money=10 #  =>Bitcoins are 10
    def value():
        if Supreme.money==0:
            value=Supreme.stocks
        elif Supreme.stocks==0:
            value=Supreme.money
        else:
            value=1
        return value


