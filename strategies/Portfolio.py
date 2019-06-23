# from .Strategy import Strategy
# from .Z import Z
#
# class Portfolio(Strategy,Z):
# def profit2(df,dfcol):
#         df['sigvol'] =  np.where((df['signal']!='None'), (Z.money/df[dfcol]) , 0)
#         df['bought']=np.where(df['signal']=='buy' , df['sigvol']*df[dfcol] , 0)
#         df['sold']=np.where(df['signal']=='sell' , df['sigvol']*df[dfcol] , 0)
#         net=df['sold'].sum()-df['bought'].sum()
#         return net

    # def pfmanage(df):
    #     df['signal']=='buy'

