import sqlite3
import time
import pandas as pd
from datetime import timedelta
from timeloop import Timeloop

from stock_trading.strategies.MAOMA import MAOMA
from stock_trading.strategies.Portfolio import Portfolio


# from ..strategies.MAOMA import MAOMA
# from ..strategies.Portfolio import Portfolio


class Trading:
    """

    """

    def __init__(self):
        pass

    counter = 0

    @classmethod
    def get_next_db(cls, df):
        """

        @param df:
        @return:
        """
        Trading.counter += 1
        i = (Trading.counter - 1) + 1000
        j = Trading.counter + 1000
        return df[i:j]

    @classmethod
    def driver(cls):
        """

        @return:
        """
        cnx = sqlite3.connect('./api/api.db')
        df = pd.read_sql_query("SELECT * FROM binance_data", cnx)

        df['Open_time'] = pd.to_datetime(df['Open_time'])
        df['Close_time'] = pd.to_datetime(df['Close_time'])
        df.rename(columns={'Open_time': 'Date'}, inplace=True)
        df = df.drop(columns=['Quote_asset_volume', 'Buy_base_asset', 'Buy_quote_asset', 'Ignore'])
        Trading.counter = 0

        start_time = df['Date'].iloc[0]
        last_index = df.shape[0] - 1
        end_time = df['Date'].iloc[last_index]

        tl = Timeloop()

        @tl.job(interval=timedelta(seconds=2))
        def paper_trade():
            """


            @param start_time:
            @param end_time:
            @return:
            """
            sliceddf = Trading.get_next_db(df)
            last_date = sliceddf['Date'].iloc[sliceddf.shape[0] - 1]
            temp = MAOMA.maomasig(sliceddf, start_time, end_time, 'Close', 30, 60)
            net = Portfolio.pfmanage(temp, 'Close')
            print("portfolio value: ", net)
            print("last date is : ", last_date)

        tl.start()
        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                tl.stop()
                break


if __name__ == '__main__':
    print('Executing as standalone script')
    print(Trading.driver())
