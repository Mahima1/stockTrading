#     startdate=pd.to_datetime(14,origin=startdate,unit='D')
# def profit(df, dfcol):
#     df['sigvol'] = np.where((df['signal'] != 'None'), 10, 0)  # Z.money/df[dfcol]
#     df['bought'] = np.where(df['signal'] == 'buy', df['sigvol'] * df[dfcol], 0)
#     df['sold'] = np.where(df['signal'] == 'sell', df['sigvol'] * df[dfcol], 0)
#     net = df['sold'].sum() - df['bought'].sum()
#     return net

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mpl_finance as candle


class Strategy:
    names = []
    datecol = 'Date'

    @classmethod
    def slicebydate(cls, df, startdate, enddate):
        temp = df[df[Strategy.datecol] >= startdate][df[Strategy.datecol] <= enddate]
        return temp

    @classmethod
    def candlesticks(cls, df, startdate, enddate):
        quotes = Strategy.slicebydate(df, startdate, enddate)
        fig, ax = plt.subplots()
        #     candle.candlestick2_ohlc(ax,quotes['Open'],quotes['High'],quotes['Low'],quotes['Close'],width=0.6,colorup='#53AA03',colordown="#C20074")
        candle.candlestick2_ohlc(ax, quotes['Open'], quotes['High'], quotes['Low'], quotes['Close'], width=0.6,
                                 colorup='#10069D', colordown="#34E5DA")  # color up is blue and down is cyan
        xdate = [i.to_pydatetime() for i in quotes['Date']]
        ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

        def mydate(x, pos):
            try:
                return xdate[int(x)]
            except IndexError:
                return ''

        ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
        fig.autofmt_xdate()
        plt.plot()

    def __init__(self):
        pass
