import sqlite3
import pandas as pd
import time
from timeloop import Timeloop
from datetime import timedelta
from stockTrading.strategies.MAOMA import MAOMA
from stockTrading.strategies.Portfolio import Portfolio


class paper_trading:
    '''

    '''
    def get_new_db(self, df):
        '''

        @param df:
        @return:
        '''
        paper_trading.get_new_db.counter += 1
        i = paper_trading.get_new_db.counter + 1000
        return df[:i]

    def driver(self):
        '''

        @return:
        '''
        cnx = sqlite3.connect('./api/api.db')
        df = pd.read_sql_query("SELECT * FROM binance_data", cnx)

        df['Open_time'] = pd.to_datetime(df['Open_time'])
        df['Close_time'] = pd.to_datetime(df['Close_time'])
        df.rename(columns={'Open_time': 'Date'}, inplace=True)
        df = df.drop(columns=['Quote_asset_volume', 'Buy_base_asset', 'Buy_quote_asset', 'Ignore'])
        paper_trading.get_new_db.counter = 0

        # df=pd.read_pickle("./api/df_of_10k_samples_ETHBTC_2019-06-24 17:39:00_2019-07-01 16:09:00.pkl")
        starttime = df['Date'].iloc[0]
        lastindex = df.shape[0] - 1
        endtime = df['Date'].iloc[lastindex]

        paper_trading.paper_trade(starttime, endtime);

    def paper_trade(self, starttime, endtime):
        '''

        @param starttime:
        @param endtime:
        @return:
        '''
        sliceddf = paper_trading.get_new_db(df)
        lastdate = sliceddf['Date'].iloc[sliceddf.shape[0] - 1]
        #     temp,lastSig=MAOMA.maomasig(sliceddf,starttime,endtime,'Close',30,60)
        #     net,totalbuysig,totalsellsig=Portfolio.pfmanage(temp,'Close')
        #     print ("portfolio value: {}   Buy sigs: {}   Sell sigs: {} ".format(net,totalbuysig,totalsellsig))
        #     print("last date is : "+str(lastdate)+"  last signal is: "+str(lastSig))
        temp = MAOMA.maomasig(sliceddf, starttime, endtime, 'Close', 30, 60)
        net = Portfolio.pfmanage(temp, 'Close')
        print("portfolio value: ", net)
        print("last date is : ", lastdate)

        # tl.start(block=True)

        tl = Timeloop()

        @tl.job(interval=timedelta(seconds=2))

        tl.start()
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                tl.stop()
                break
