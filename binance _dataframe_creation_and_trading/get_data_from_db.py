'''
Getting data from exchange's api and converting it into a dataframe consisting of columns and that too in the same order as given below:
["Open_time", "Open", "High","Low","Close", "Volume","Close_time","Quote_asset_volume","Number_of_trades","Buy_base_asset","Buy_quote_asset","Ignore"]
All columns having python date or time as datatypes are expected to be in timestamp format.

binance github api link
https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
'''

# import sqlite3
# import pandas as pd
#
# cnx=sqlite3.connect('./api/api.db')
# df = pd.read_sql_query("SELECT * FROM binance_data", cnx)
#
# df['Open_time']=pd.to_datetime(df['Open_time'])
# df['Close_time']=pd.to_datetime(df['Close_time'])
# df.rename(columns={'Open_time':'Date'}, inplace=True)
# df=df.drop(columns=['Quote_asset_volume','Buy_base_asset','Buy_quote_asset','Ignore'])

# def make_db(coinSymbol, klineInterval, noSamples):
#     '''
#
#     @param coinSymbol:
#     @param klineInterval:
#     @param noSamples:
#     @return:
#     '''
#     import pandas as pd
#     import datetime
#     import requests
#
#     params = {'symbol': coinSymbol, 'interval': klineInterval, 'limit': limit}
#     apiResponse = requests.get('https://api.binance.com/api/v1/klines', params)
#     #     td is timeDifference, it is being used to calculate first date and last date from given dataframe so you dont have to provide it exclusively
#     td = df['Date'].iloc[999] - df['Date'].iloc[0]
#     starttime = int(datetime.datetime.timestamp(df['Date'].iloc[0] - 10 * (td))) * 1000
#     endtime = int(datetime.datetime.timestamp(df['Date'].iloc[0] - 9 * (td))) * 1000
#     #     print(starttime,endtime)
#     params = {'symbol': coinSymbol, 'startTime': starttime, 'endTime': endtime, 'interval': klineInterval,
#               'limit': limit}
#     apiResponse = requests.get('https://api.binance.com/api/v1/klines', params)
#     maindf = pd.DataFrame.from_records(apiResponse.json())
#     maindf.columns = ["Open_time", "Open", "High", "Low", "Close", "Volume", "Close_time", "Quote_asset_volume",
#                       "Number_of_trades", "Buy_base_asset", "Buy_quote_asset", "Ignore"]
#
#     for i in range(9, 0, -1):
#         starttime = int(datetime.datetime.timestamp(df['Date'].iloc[0] - i * (td))) * 1000
#         endtime = int(datetime.datetime.timestamp(df['Date'].iloc[0] - (i - 1) * (td))) * 1000
#         params = {'symbol': coinSymbol, 'startTime': starttime, 'endTime': endtime, 'interval': klineInterval,
#                   'limit': limit}
#         apiResponse = requests.get('https://api.binance.com/api/v1/klines', params)
#         temp = pd.DataFrame.from_records(apiResponse.json())
#         temp.columns = ["Open_time", "Open", "High", "Low", "Close", "Volume", "Close_time", "Quote_asset_volume",
#                         "Number_of_trades", "Buy_base_asset", "Buy_quote_asset", "Ignore"]
#         maindf = maindf.append(temp, ignore_index=True)
#
#     return maindf
