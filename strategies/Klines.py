from stock_trading.strategies.Strategy import Strategy
from stock_trading.strategies.MA import MA


class Klines(Strategy):
    """
    Candlestick charts are a technical tool that packs data for multiple time frames into single price bars.
    This makes them more useful than traditional open-high, low-close bars or simple lines that connect the dots of closing prices.
    Candlesticks build patterns that predict price direction once completed.
    """
    Strategy.names.append('Doji')
    Strategy.names.append('Umbrella')
    Strategy.names.append('Moribozu')

    def __init__(self):
        super(Strategy, self).__init__()

    @classmethod
    def doji(cls, df, startdate, enddate, dfcol, window):
        """
        Basic Info and Implementation:
        A doji is a name for a session in which the candlestick for a security has an open and close that are virtually equal and
        are often components in patterns.Alone, doji are neutral patterns that are also featured in a number of important patterns.
        Here if after a trend (positive or negative) doji appears then we consider it being a somewhat valid signal.
        Implemented by first filtering out samples which follow a trend and trend is seen by taking slope of every 5 samples
        and if it greater than 0.6 , its a trend (+ and - both) .

        Formulae :
        slope of every 5 samples >= 0.6
        open - close / high - low <= 0.3
        similarly ratios of high-open and high-close are set

        Doji tell us:
        Since High / low are farther as compared to Open / close as prices have differed greatly but at the end of day
        remained same this implies that their is confusion in the market and it has been more volatile than usual.
        So it is more risky.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date, format ('YYYY-MM-DD')
        @param enddate: Date, format ('YYYY-MM-DD')
        @param dfcol: String, Name of dataframe column on which to apply this analytics like 'Close' or 'Open'
        @param window: int, Number of days in smoothing period
        @return: Dataframe with only those samples which make this pattern
        """
        q1 = MA.moving_average(df, startdate, enddate, dfcol, window)
        q3 = q1.copy()
        q1['shiftedroll'] = q1['roll'].shift(5)
        q3['slope'] = (q1['roll'] - q1['shiftedroll']) / 5
        q3 = q3[abs(q3['slope']) >= 0.6]
        q3 = q3[(abs((q1['High'] - q1['Open']) / (q1['Close'] - q1['Low']))) >= 0.8]
        q3 = q3[(abs((q1['High'] - q1['Open']) / (q1['Close'] - q1['Low']))) <= 1.25]
        q3 = q3[abs((q3['Open'] - q3['Close']) / (q3['High'] - q3['Low'])) <= 0.3]
        return q3

    #     print(q3)# if -ve denotes downward trend

    @classmethod
    def umbrella(cls, df, startdate, enddate, dfcol, window):
        """
        Basic Info and Implementation:
        Candlestick Umbrella pattern is a kind of a doji with no upper shadow but a long lower shadow.
        The lower long shadow shows the evidence for buying pressure. The low price position indicates
        that plenty of sellers still are around. Umbrella candle pattern is interpreted as a reversal pattern.

        Umbrella is meaningful if it comes with a trend hence to generate signals with it, first slope of samples is calculated and if it is >0.6 then we checked if umbrella if formed or not by looking at ratios and determining two things -  one being that  candlestick body of sample is smaller as compared to high/low line segment and other being line segment above body is smaller than the one below the body.

        @param df: Dataframe object with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @param dfcol: String, Name of dataframe column on which to apply this analytics like 'Close' or 'Open'
        @param window: int, number of days to use in analysis
        @return: dataframe object filtered with only those samples which create a meaningful umbrella

        """
        q1 = MA.moving_average(df, startdate, enddate, dfcol, window)
        q3 = q1.copy()
        q1['shiftedroll'] = q1['roll'].shift(5)
        q3['slope'] = (q1['roll'] - q1['shiftedroll']) / 5
        q3 = q3[abs(q3['slope']) >= 0.6]
        q3 = q3[abs((q3['Open'] - q3['Close']) / (q3['High'] - q3['Low'])) <= 0.3]
        q3 = q3[(abs((q1['Close'] - q1['Low']) / (q1['High'] - q1['Open']))) >= 2]
        return q3

    @classmethod
    def maribozu(cls, df, startdate, enddate):
        """
        The marubozu is simply a long black candle, with little to no upper or lower shadows.
        The pattern shows that sellers controlled the trading day from open to close, and is therefore a bearish pattern .
        This func calculates the ratio of difference of 'open','close' and difference of 'high','low' and filters out those with ratio >0.95 hence we get samples with big body.

        @param df: Dataframe with at least these 5 columns in it namely - [High, Open, Low, Close, Date]
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @return: Dataframe with only maribozu making samples
        """

        temp = Strategy.slicebydate(df, startdate, enddate)
        temp2 = temp[abs((temp['Open'] - temp['Close']) / (temp['High'] - temp['Low'])) >= 0.95]
        return temp2

    @classmethod
    def plotit(cls, t, startdate, enddate):
        """
        Function for plotting bands in a time series graph.

        @param t: Dataframe returned from candlesticks function of the Strategy module
        @param startdate: Date ('YYYY-MM-DD')
        @param enddate: Date ('YYYY-MM-DD')
        @return: void
        """
        Strategy.candlesticks(t, startdate, enddate)
#
# Klines.doji(spy,'2007-08-08','2008-10-10')
# Klines.umbrella(spy,'2007-08-08','2008-10-10')
# Klines.maribozu(spy,'2007-08-08','2011-10-10')
