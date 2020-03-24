import sqlite3
import time
from datetime import timedelta

import pandas as pd
from strategies.MAOMA import MAOMA
from timeloop import Timeloop


# from stockTrading.strategies.Portfolio import Portfolio


class Trading:

    def get_new_db(self, df):
        """

        @param df:
        @return:
        """
        Trading.get_new_db.counter += 1
        i = Trading.get_new_db.counter + 1000
        return df[:i]

    def driver(self):
        """

        @return:
        """
        cnx = sqlite3.connect('./api/api.db')
        df = pd.read_sql_query("SELECT * FROM binance_data", cnx)

        df['Open_time'] = pd.to_datetime(df['Open_time'])
        df['Close_time'] = pd.to_datetime(df['Close_time'])
        df.rename(columns={'Open_time': 'Date'}, inplace=True)
        df = df.drop(columns=['Quote_asset_volume', 'Buy_base_asset', 'Buy_quote_asset', 'Ignore'])
        Trading.get_new_db.counter = 0

        # df=pd.read_pickle("./api/df_of_10k_samples_ETHBTC_2019-06-24 17:39:00_2019-07-01 16:09:00.pkl")

        starttime = df['Date'].iloc[0]
        lastindex = df.shape[0] - 1
        endtime = df['Date'].iloc[lastindex]

        # tl.start(block=True)

        tl = Timeloop()

        @tl.job(interval=timedelta(seconds=2))
        def paper_trade(starttime, endtime):
            """


            @param starttime:
            @param endtime:
            @return:
            """
            sliceddf = Trading.get_new_db(df)
            lastdate = sliceddf['Date'].iloc[sliceddf.shape[0] - 1]
            #     temp,lastSig=MAOMA.maomasig(sliceddf,starttime,endtime,'Close',30,60)
            #     net,totalbuysig,totalsellsig=Portfolio.pfmanage(temp,'Close')
            #     print ("portfolio value: {}   Buy sigs: {}   Sell sigs: {} ".format(net,totalbuysig,totalsellsig))
            #     print("last date is : "+str(lastdate)+"  last signal is: "+str(lastSig))
            temp = MAOMA.maomasig(sliceddf, starttime, endtime, 'Close', 30, 60)
            net = Portfolio.pfmanage(temp, 'Close')
            print("portfolio value: ", net)
            print("last date is : ", lastdate)

        tl.start()
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                tl.stop()
                break

    # def __init__(self):
    #     print("paper_trading class")
