import datetime

import pandas as pd
import requests


# import sys
# sys.path.append('/home/r/stockTrading/')
# from stockTrading.strategies.MACD import MACD
# from stockTrading.strategies.Boll import Boll
# from stockTrading.strategies.Join import join, optimizer
# from stockTrading.strategies.Rsi import Rsi
# from stockTrading.strategies.Vol import Vol
# from stockTrading.strategies.MAOMA import MAOMA

class Backtesting:
    """

    """

    coinSymbols = ['XMRBTC', 'ETHBTC', 'NEOBTC', 'BTCUSDT', 'LTCBTC']
    klineInterval = '1m'

    def convert_response_to_df_for_backtesting(self, api_response):
        """

        @param api_response:
        @return:
        """
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

    def make_df(self, coin_symbol, kline_interval):
        """

        @param coin_symbol:
        @param kline_interval:
        @return:
        """
        #     coin_symbol='LTCBTC'
        #     kline_interval='1m'
        limit = 1000
        params = {'symbol': coin_symbol, 'interval': kline_interval, 'limit': limit}
        api_response = requests.get('https://api.binance.com/api/v1/klines', params)

        df = Backtesting.convert_response_to_df_for_backtesting(api_response)
        #     td is timeDifference, it is being used to calculate first date and last date from given dataframe so you dont have to provide it exclusively
        td = df['Date'].iloc[999] - df['Date'].iloc[0]
        starttime = int(datetime.datetime.timestamp(df['Date'].iloc[0] - 10 * td)) * 1000
        endtime = int(datetime.datetime.timestamp(df['Date'].iloc[0] - 9 * td)) * 1000
        params = {'symbol': coin_symbol, 'startTime': starttime, 'endTime': endtime, 'interval': kline_interval,
                  'limit': limit}
        api_response = requests.get('https://api.binance.com/api/v1/klines', params)
        maindf = pd.DataFrame.from_records(api_response.json())
        maindf.columns = ["Open_time", "Open", "High", "Low", "Close", "Volume", "Close_time", "Quote_asset_volume",
                          "Number_of_trades", "Buy_base_asset", "Buy_quote_asset", "Ignore"]

        for i in range(9, 0, -1):
            starttime = int(datetime.datetime.timestamp(df['Date'].iloc[0] - i * td)) * 1000
            endtime = int(datetime.datetime.timestamp(df['Date'].iloc[0] - (i - 1) * td)) * 1000
            params = {'symbol': coin_symbol, 'startTime': starttime, 'endTime': endtime, 'interval': kline_interval,
                      'limit': limit}
            api_response = requests.get('https://api.binance.com/api/v1/klines', params)
            temp = pd.DataFrame.from_records(api_response.json())
            temp.columns = ["Open_time", "Open", "High", "Low", "Close", "Volume", "Close_time", "Quote_asset_volume",
                            "Number_of_trades", "Buy_base_asset", "Buy_quote_asset", "Ignore"]
            maindf = maindf.append(temp, ignore_index=True)
            maindf.rename(columns={'Open_time': 'Date'}, inplace=True)
        return maindf

    def back_test(self, coin_symbol, kline_interval):
        """

        @param coin_symbol:
        @param kline_interval:
        @return:
        """

        df = Backtesting.make_df(coin_symbol, kline_interval)
        starttime = df['Date'].iloc[0]
        lastindex = df.shape[1]
        endtime = df['Date'].iloc[lastindex]

        arr1 = [[5, 30], [40, 100]]
        arr2 = [[10, 20], [2, 4]]
        arr3 = [[5, 30], [40, 100]]
        arr4 = [[60, 95], [5, 40], [5, 30]]
        arr5 = [[10, 40]]

        llist = [
            MACD.macdoptimize(df, starttime, endtime, 'Close', arr1),
            Boll.boloptimize(df, starttime, endtime, arr2),
            MAOMA.maomaoptimize(df, starttime, endtime, 'Close', arr3),
            Rsi.rsioptimize(df, starttime, endtime, 'Close', arr4),
            Vol.voloptimize(df, starttime, endtime, arr5)
        ]

        return optimizer(llist)

    for i in range(len(coinSymbols)):
        back_test(coinSymbols[i], klineInterval)
