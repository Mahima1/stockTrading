import sqlite3
import time
import pandas as pd
from datetime import timedelta
from timeloop import Timeloop

from stock_trading.strategies.MAOMA import MAOMA
from stock_trading.strategies.Portfolio import Portfolio


class Trading:

    def __init__(self):
        pass

    counter = 0

    @classmethod
    def get_next_db(cls, df):
        """
        @param df: Dataframe with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @return:
        """
        nos_of_samples = 100
        Trading.counter += 1
        i = (Trading.counter - 1) * nos_of_samples
        j = Trading.counter * 100
        return df[i:j]

    @classmethod
    def driver(cls):

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
            sliced_df = Trading.get_next_db(df)
            last_date = sliced_df['Date'].iloc[sliced_df.shape[0] - 1]
            temp = MAOMA.maomasig(sliced_df, start_time, end_time, 'Close', 5, 15)
            net = Portfolio.pf_manage(temp, 'Close')
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
