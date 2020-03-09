#     startdate=pd.to_datetime(14,origin=startdate,unit='D')
# def profit(df, dfcol):
#     df['sigvol'] = np.where((df['signal'] != 'None'), 10, 0)  # Z.money/df[dfcol]
#     df['bought'] = np.where(df['signal'] == 'buy', df['sigvol'] * df[dfcol], 0)
#     df['sold'] = np.where(df['signal'] == 'sell', df['sigvol'] * df[dfcol], 0)
#     net = df['sold'].sum() - df['bought'].sum()
#     return net

import numpy as np
import mpl_finance as candle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class Strategy:
    names = []
    datecol = 'Date'

    def rsisig(self, df, startdate, enddate, upperlimit, lowerlimit, window):
        raise NotImplementedError("Function not implemented here")

    def bolsig(self, df, window, startdate, enddate):
        raise NotImplementedError("Function not implemented here")

    def volsig(self, df, window, startdate, enddate):
        raise NotImplementedError("Function not implemented here")

    def slicebydate(self, df, startdate, enddate):
        temp = df[df[Strategy.datecol] >= startdate][df[Strategy.datecol] <= enddate]
        return temp

    def candlesticks(self, df, startdate, enddate):
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

    def __init__(self, df, startdate, enddate):
        self.df = df
        self.startdate = startdate
        self.enddate = enddate
