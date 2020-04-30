import datetime
import pandas as pd
import requests

from stock_trading.strategies.Boll import Boll
from stock_trading.strategies.Join import Join
from stock_trading.strategies.MACD import MACD
from stock_trading.strategies.MAOMA import MAOMA
from stock_trading.strategies.Rsi import Rsi
from stock_trading.strategies.Vol import Vol


class Backtesting:
    """

    """

    coin_symbols = ['XMRBTC', 'ETHBTC', 'NEOBTC', 'BTCUSDT', 'LTCBTC']
    kline_interval = '1m'

    def __init__(self):
        pass

    @classmethod
    def convert_response_to_df_for_backtesting(cls, api_response):
        """

        @param api_response:
        @return:
        """
        print("Converting response from api to dataframe")
        df = pd.DataFrame.from_records(api_response.json())
        df.columns = ["Open_time", "Open", "High", "Low", "Close", "Volume", "Close_time", "Quote_asset_volume",
                      "Number_of_trades", "Buy_base_asset", "Buy_quote_asset", "Ignore"]
        df_dict = df.to_dict('records')
        l = len(df_dict)
        for i in range(l):
            df_dict[i]['Close_time'] = datetime.datetime.fromtimestamp((df_dict[i]['Close_time']) / 1000)
            df_dict[i]['Open_time'] = datetime.datetime.fromtimestamp((df_dict[i]['Open_time']) / 1000)
        df = pd.DataFrame(df_dict)
        df.rename(columns={'Open_time': 'Date'}, inplace=True)
        return df

    @classmethod
    def make_timedelta(cls, coin_symbol, kline_interval):

        limit = 1000
        params = {'symbol': coin_symbol, 'interval': kline_interval, 'limit': limit}
        api_response = requests.get('https://api.binance.com/api/v1/klines', params)

        df = Backtesting.convert_response_to_df_for_backtesting(api_response)
        td = df['Date'].iloc[999] - df['Date'].iloc[0]
        start_time = int(datetime.datetime.timestamp(df['Date'].iloc[0] - 10 * (td))) * 1000
        end_time = int(datetime.datetime.timestamp(df['Date'].iloc[0] - 9 * (td))) * 1000
        params = {'symbol': coin_symbol, 'startTime': start_time, 'endTime': end_time, 'interval': kline_interval,
                  'limit': limit}
        api_response = requests.get('https://api.binance.com/api/v1/klines', params)
        maindf = pd.DataFrame.from_records(api_response.json())

        maindf.columns = ["Open_time", "Open", "High", "Low", "Close", "Volume", "Close_time", "Quote_asset_volume",
                          "Number_of_trades", "Buy_base_asset", "Buy_quote_asset", "Ignore"]
        maindf.rename(columns={'Open_time': 'Date'}, inplace=True)
        cols = maindf.columns[maindf.dtypes.eq('object')]
        maindf[cols] = maindf[cols].apply(pd.to_numeric)
        return maindf, df, td

    @classmethod
    def make_df_for_backtesting(cls, coin_symbol, kline_interval):
        print("Making dataframe bigger")
        limit = 1000
        maindf, df, td = Backtesting.make_timedelta(coin_symbol, kline_interval)

        for i in range(9, 0, -1):
            start_time = int(datetime.datetime.timestamp(df['Date'].iloc[0] - i * (td))) * 1000
            end_time = int(datetime.datetime.timestamp(df['Date'].iloc[0] - (i - 1) * (td))) * 1000
            params = {'symbol': coin_symbol, 'startTime': start_time, 'endTime': end_time, 'interval': kline_interval,
                      'limit': limit}
            api_response = requests.get('https://api.binance.com/api/v1/klines', params)
            temp = pd.DataFrame.from_records(api_response.json())
            temp.columns = ["Open_time", "Open", "High", "Low", "Close", "Volume", "Close_time", "Quote_asset_volume",
                            "Number_of_trades", "Buy_base_asset", "Buy_quote_asset", "Ignore"]
            temp.rename(columns={'Open_time': 'Date'}, inplace=True)
            cols = temp.columns[temp.dtypes.eq('object')]
            temp[cols] = temp[cols].apply(pd.to_numeric)
            maindf = maindf.append(temp, ignore_index=True)
        return maindf

    @classmethod
    def driver(cls, coin_symbol, kline_interval):
        """

        @param coin_symbol:
        @param kline_interval:
        @return:
        """

        print("Running tests...")

        df = Backtesting.make_df_for_backtesting(coin_symbol, kline_interval)
        start_time = df['Date'].iloc[0]
        last_index = df.shape[1]
        end_time = df['Date'].iloc[last_index]

        arr1 = [[5, 30], [40, 100]]
        arr2 = [[10, 20], [2, 4]]
        arr3 = [[5, 30], [40, 100]]
        arr4 = [[60, 95], [5, 40], [5, 30]]
        arr5 = [[10, 40]]

        optimize_func_list = [
            MACD.macdoptimize(df, start_time, end_time, 'Close', arr1),
            Boll.boloptimize(df, start_time, end_time, arr2),
            MAOMA.maomaoptimize(df, start_time, end_time, 'Close', arr3),
            Rsi.rsioptimize(df, start_time, end_time, 'Close', arr4),
            Vol.voloptimize(df, start_time, end_time, arr5)
        ]

        return Join.optimizer(optimize_func_list)

    @classmethod
    def back_test(cls):
        print("Backtesting func started...")
        # for i in range(len(Backtesting.coin_symbols)):
        #     print(Backtesting.driver(Backtesting.coin_symbols[i], Backtesting.kline_interval))
        print(Backtesting.driver(Backtesting.coin_symbols[0], Backtesting.kline_interval))
