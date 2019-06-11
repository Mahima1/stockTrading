#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


def csvreader(path):
    return pd.read_csv(path,parse_dates=['Date'],infer_datetime_format=True)
    
spy=csvreader("./SPY.csv")
google=csvreader("./GOOG.csv")
apple=csvreader("./AAPL.csv")
ibm=csvreader("./IBM.csv")
fb=csvreader("./FB.csv")
tesla=csvreader("./TSLA.csv")

def norm(df,dfcol):
    df[dfcol+'norm']=df[dfcol]/df[dfcol].iloc[0]
    return df

z=pd.DataFrame()
spy=norm(spy,'Adj Close')
google=norm(google,'Adj Close')
plt.plot(spy['Adj Closenorm'])
plt.plot(google['Adj Closenorm'])


# In[3]:


# import time
# zz=time.time()
# a=spy['Adj Close']
# for i in range(2516):
#     a.iloc[i]/a.iloc[0]
# timedif=time.time()-zz
# print ("in for loop: ",timedif)

# xx=time.time()
# y=google['Adj Close']
# y/y.iloc[0]
# timediff=time.time()-xx
# print ("pandas: ",timediff)

# print(timedif/timediff)


# In[4]:


#def findreturn(df):
 #  str=
z['spydr']=((spy['Adj Close'].shift(1)-spy['Adj Close'])/spy['Adj Close'])*100
z['googledr']=((google['Adj Close'].shift(1)-google['Adj Close'])/google['Adj Close'])*100
z['googledate']=google['Date']
#temp['spyadjtoday']
z.plot(x='googledate')


# In[5]:


import numpy as np
x=z['spydr'].dropna()
y=z['googledr'].dropna()
eq=np.polyfit(x,y,1)
print (eq)


# In[6]:


def plotline(eq):
    x = np.linspace(-15,10,100)
    m=eq[0]
    c=eq[1]
    y = m*x+c
    plt.plot(x, y, '-r', label='y=mx+c')
    
plt.plot(z['spydr'],z['googledr'])
plotline(eq)


# In[7]:


def slicebydate(df,dfcol,datecol,startdate, enddate):
    temp=pd.DataFrame()
    temp[dfcol]=df[dfcol][df[datecol]>=startdate][df[datecol]<=enddate]
    temp[datecol]=df[datecol][df[datecol]>=startdate][df[datecol]<=enddate]
    temp.plot(x=datecol,y=dfcol)
#     return temp
# slicebydate(apple,'Adj Close','Date','2017-01-01','2017-05-30')

def slicebydate2(df,datecol,startdate, enddate):
    temp=df[df[datecol]>=startdate][df[datecol]<=enddate]
    return temp


# In[31]:


# pd.to_datetime(1,origin=datetime.date(2017,5,2),unit='D')
#     temp[dfcol+' predicted']=temp.rolling(window)[dfcol].mean()
    
#     temp[dfcol+' new']=temp[dfcol+' new'].shift(1)
#     temp=temp.fillna(0)
#     temp[dfcol]=temp[dfcol]+temp[dfcol+' new']
#        print(temp['new ewm'].tail(100))

# def moving_average(df,dfcol,window,days):
#     temp=pd.DataFrame()
#     temp2=pd.DataFrame()
#     temp[dfcol]=df[dfcol][::-1][:500]
#     temp['Date']=df['Date'][::-1][:500]
#     temp=temp[::-1]
    
#     lastdate=df['Date'].iloc[-1]
#     temp2['Date']=pd.date_range(start=pd.to_datetime(1,origin=lastdate,unit='D'),end=pd.to_datetime(days,origin=lastdate,unit='D'))
#     temp=temp.append(temp2,ignore_index=True)
#     temp['new roll']=temp.rolling(window, min_periods = 1)[dfcol].mean()
#     temp['new ewm']=temp.ewm(com=3)[dfcol].mean()
#     temp['std']=temp.rolling(window, min_periods = 1)[dfcol].std()
#     temp['upper band']=temp['new roll']+(2*temp['std'])
#     temp['lower band']=temp['new roll']-(2*temp['std'])

#     plt.plot(temp['Date'],temp['new roll'])
#     plt.plot(df['Date'][2480:],df[dfcol][2480:])
#     plt.plot(temp['Date'],temp['new ewm'])
#     plt.plot(temp['Date'],temp['upper band'])
#     plt.plot(temp['Date'],temp['lower band'])
    
# moving_average(apple,'Adj Close',50,10)

def moving_average2(df,dfcol,window,days,startdate,enddate):
    import datetime
    temp=slicebydate2(df,'Date',startdate,enddate)
    temp2=pd.DataFrame()
    temp2['Date']=pd.date_range(start=pd.to_datetime(1,origin=enddate,unit='D'),end=pd.to_datetime(days,origin=enddate,unit='D'))
    temp=temp.append(temp2,ignore_index=True)
    temp['roll']=temp.rolling(window, min_periods = 1)[dfcol].mean()
    return temp
#     plt.plot(temp['Date'],temp['roll'])
    
def bollinger_bands(df,window,days,startdate,enddate):
    temp=df
    temp['typical price']=(temp['Close']+temp['High']+temp['Low'])/3
    temp=moving_average2(temp,'typical price',window,days,startdate,enddate)
    temp['std']=temp.rolling(window, min_periods = 1)['typical price'].std()
    temp['upper band']=temp['roll']+(3*temp['std'])
    temp['lower band']=temp['roll']-(3*temp['std'])
    return temp
#     plt.plot(temp['Date'],temp['typical price'])
#     plt.plot(temp['Date'],temp['upper band'])
#     plt.plot(temp['Date'],temp['lower band'])
    
# moving_average2(spy,'Adj Close',20,20,'2007-09-09','2007-10-10')
bollinger_bands(spy,20,1,'2007-09-09','2007-10-10')


# In[9]:


# a=spy[['Date','Open','High','Low','Close']][:100]
# a['Date'] = pd.to_datetime(a['Date'])
# a["Date"] = a["Date"].apply(mdates.date2num)
# quotes=a[['Date','Open','High','Low','Close']].copy()
# fig,ax=plt.subplots()
# #candle.candlestick2_ohlc(ax,quotes['Open'],quotes['High'],quotes['Low'],quotes['Close'])
# candle.candlestick_ohlc(ax,quotes.values)
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# quotes=slicebydate(spy,'Open','Date','2017-01-01','2017-05-30')
# quotes=spy[['Date','Open','High','Low','Close']][spy['Date']<'2007-07-07']

def candlesticks(df,startdate,enddate):
    import mpl_finance as candle
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    import datetime as datetime
    quotes=slicebydate2(df,'Date',startdate,enddate)
    fig, ax = plt.subplots()
    candle.candlestick2_ohlc(ax,quotes['Open'],quotes['High'],quotes['Low'],quotes['Close'],width=0.6,colorup='#53AA03',colordown="#C20074")
#     candle.candlestick2_ohlc(ax,quotes['Open'],quotes['High'],quotes['Low'],quotes['Close'],width=0.6,colorup='#10069D',colordown="#34E5DA")
    xdate = [i.to_pydatetime() for i in quotes['Date']]
    
    #xdate = quotes['Date']
    ax.xaxis.set_major_locator(ticker.MaxNLocator(6))
    def mydate(x,pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
    fig.autofmt_xdate()
#     fig.tight_layout()
    plt.plot()

candlesticks(spy,'2007-08-08','2007-10-10')


# In[10]:


def macd(df,dfcol,window1,window2,days,startdate,enddate):
    t1=moving_average2(df,dfcol,window1,days,startdate,enddate)
    t2=moving_average2(df,dfcol,window2,days,startdate,enddate)
#     plt.plot(t1['Date'],t1['roll'])
#     plt.plot(t2['Date'],t2['roll'])
    return t1,t2
# macd(spy,'Adj Close',15,100,10,'2007-08-08','2008-12-12')


# In[11]:


def movmov(df,dfcol,window1,window2,days,startdate,enddate):
    t1=moving_average2(df,dfcol,window1,days,startdate,enddate)
    t2=moving_average2(t1,'roll',window2,days,startdate,enddate)
#     plt.plot(t1['Date'],t1['roll'])
#     plt.plot(t2['Date'],t2['roll'])
    return t1,t2
# print(movmov(spy,'Adj Close',15,15,1,'2007-08-08','2008-12-12'))


# In[22]:


macd(spy,'Adj Close',15,60,10,'2007-08-08','2008-12-12')
bollinger_bands(spy,15,10,'2007-08-08','2008-12-12')


# In[13]:


trades=[{'type':'buy', 'volume':500, 'date':'2013-09-09'},
       {'type':'sell', 'volume':300, 'date':'2014-09-09'},
       {'type':'sell' , 'volume':200, 'date':'2015-09-09'}]

def profit():
    #tradesdf.drop([0,1,2,3,4,5,6,7,8])
    tradesdf=pd.DataFrame(columns=['Type','Volume','Date'])
    for i in range(len(trades)):
        tradesdf.loc[i]=[trades[i]['type'],trades[i]['volume'],trades[i]['date']]
    tradesdf['Date']= pd.to_datetime(tradesdf['Date'])
    tradesdf['Adj Close']=0
    for p in range(len(trades)):
        tradesdf['Adj Close'].iloc[p]=float(spy['Adj Close'][spy['Date']==tradesdf['Date'].iloc[p]])
    tradesdf['Bought']=tradesdf['Adj Close'][tradesdf['Type']=='buy']*tradesdf['Volume'][tradesdf['Type']=='buy']
    tradesdf['Sold']=tradesdf['Adj Close'][tradesdf['Type']=='sell']*tradesdf['Volume'][tradesdf['Type']=='sell']
    net=tradesdf['Sold'].sum()-tradesdf['Bought'].sum()
    print(tradesdf,"\n")
    print("Profit is: ",net)

profit()


# In[14]:


def plotline2(eq):
    x = np.linspace(0,350,100)
    m=eq[0]
    c=eq[1]
    y = m*x+c
    plt.plot(x, y, '-r', label='y=mx+c')

def profit2(df):
    import numpy as np
    df['sigvol']=np.where((df['signal']!='None'),10,0)
    df['bought']=np.where(df['signal']=='buy' , df['sigvol']*df['Adj Close'] , 0)
    df['sold']=np.where(df['signal']=='sell' , df['sigvol']*df['Adj Close'] , 0)
    net=df['sold'].sum()-df['bought'].sum()
#     print(df[df['multiple']<0])
#     print("Profit is: ",net)
    return net
    
def indicators(q1,q2):
    import numpy as np
#   temp=q1.join(q2.set_index('roll'),on='roll',how='inner',lsuffix='_q1',rsuffix='_q2')  
#   df.join(other.set_index('key'), on='key')
    q1['diff']=q1['roll']-q2['roll']
    q1['shift']=(q1['diff'].shift(1))
    q1['multiple']=q1['diff']*q1['shift']
    mask = q1['multiple']<0
    mask1=q1['shift']>0
    where1=np.where(mask1,'buy','sell')
    q1['signal'] = np.where(mask,where1,'None')
    q1['sigvol']=np.where((q1['signal']!='None'),10,0)
    return q1
    
def whowins(r):
    import random
    flag=0
    for i in range(r):
        q1,q2=movmov(spy,'Adj Close',int(random.random()*100)+1,int(random.random()*100)+1,1,'2007-08-08','2008-12-12')
        bobu=profit2(indicators(q1,q2))
        a1,a2=macd(spy,'Adj Close',int(random.random()*100)+1,int(random.random()*100)+1,1,'2007-08-08','2008-12-12')
        gogu=profit2(indicators(a1,a2))
        if bobu>=gogu:
            flag+=1
    print ("{} many times bobu won".format(flag))

whowins(10)


# In[40]:


#   t=slicebydate2(df,'Date',startdate,enddate)
#     t['diff']=t['Adj Close'].diff()
#     t['profit']=np.where(t['diff']<0 ,0, t['diff'])
#     t['loss']=np.where(t['diff']>0 ,0, t['diff'])
#     t['profitroll']=t.rolling(window, min_periods = 1)['profit'].mean()
#     t['lossroll']=t.rolling(window, min_periods = 1)['loss'].mean().abs()
#     x=profitroll/lossroll
#     x=(x/(1+x))*100

def maribozu(df,startdate,enddate):
    temp=slicebydate2(df,'Date',startdate,enddate)
    temp2=temp[abs((temp['Open']-temp['Close'])/(temp['High']-temp['Low']))>=0.95]
    candlesticks(temp2,startdate,enddate)

def doji(df,startdate,enddate):
    q1=moving_average2(spy,'Adj Close',5,1,startdate,enddate)
    q3=q1
    q1['shiftedroll']=q1['roll'].shift(5)
    q3['slope']=(q1['roll']-q1['shiftedroll'])/5
    q3=q3[abs(q3['slope'])>=0.6]
    q3=q3[(abs((q1['High']-q1['Open'])/(q1['Close']-q1['Low'])))>=0.8]
    q3=q3[(abs((q1['High']-q1['Open'])/(q1['Close']-q1['Low'])))<=1.25]
    q3=q3[abs((q3['Open']-q3['Close'])/(q3['High']-q3['Low']))<=0.3]
#     print(q3)# if -ve denotes downward trend
    candlesticks(q3,startdate,enddate)
    
def umbrella(df,startdate,enddate):
    q1=moving_average2(spy,'Adj Close',5,1,startdate,enddate)
    q3=q1
    q1['shiftedroll']=q1['roll'].shift(5)
    q3['slope']=(q1['roll']-q1['shiftedroll'])/5
    q3=q3[abs(q3['slope'])>=0.6]
    q3=q3[abs((q3['Open']-q3['Close'])/(q3['High']-q3['Low']))<=0.3]
    q3=q3[(abs((q1['Close']-q1['Low'])/(q1['High']-q1['Open'])))>=2]
#     print(q3)# if -ve denotes downward trend
    candlesticks(q3,startdate,enddate)

def rsi(df,startdate,enddate,window):
    temp=slicebydate2(df,'Date',startdate,enddate)
    temp2=temp['Adj Close'].diff()
    profit, loss = temp2.copy(), temp2.copy()
    profit[profit < 0] = 0
    loss[loss > 0] = 0
    profitroll=profit.rolling(window, min_periods = 1).mean()
    lossroll=loss.rolling(window, min_periods = 1).mean().abs()
    x=profitroll/lossroll
    x=(x/(1+x))
    temp['rsi']=(x*100)
    return temp
#     temp.plot(x='Date',y='rsi')
    
def rsisig(df,upperlimit,lowerlimit,startdate,enddate,window):
    t=rsi(df,startdate,enddate,window)
    mask = t['rsi']<=lowerlimit
    mask1=t['rsi']>=upperlimit
    t['signal'] = np.where(mask,'buy',(np.where(mask1,'sell','None')))
#     print (t[['Date','rsi']][t['signal']=='sell'])
    return profit2(t)
#     print("Profit is: ",net)
def bolsig(df,window,days,startdate,enddate):
    t=bollinger_bands(df,window,days,startdate,enddate)
    mask1=t['High']>=t['upper band']
    mask=t['Low']<=t['lower band']
    t['signal'] = np.where(mask,'buy',(np.where(mask1,'sell','None')))
    return profit2(t)

def volsig(df,window,days,startdate,enddate):
    temp=moving_average2(df,'Volume',window,days,startdate,enddate)
    temp['%vol']=((temp['Volume']-temp['roll'])/temp['roll'])*100
    temp['signal']=np.where(temp['%vol']>=30,'buy',np.where(temp['%vol']<=-30,'sell','None'))
    return temp
#     plt.plot(temp['Date'],temp['roll'])
#     plt.plot(temp['Date'],temp['Volume'])
# rsi(google,'2008-01-01','2008-10-10',30)
# umbrella(spy,'2007-08-08','2008-10-10')
# doji(spy,'2007-08-08','2008-10-10')
# maribozu(spy,'2007-08-08','2011-10-10')
# candlesticks(spy,'2008-01-01','2008-10-10')
# bollinger_bands(spy,15,1,'2008-01-01','2008-10-10')
# bolsig(google,20,1,'2008-01-01','2008-10-10')
# rsisig(google,60,20,'2008-01-01','2008-10-10',30)
volsig(spy,5,1,'2008-01-01','2008-10-10')


# In[27]:


# bollinger_bands(spy,15,1,'2008-01-01','2008-10-10')
# t=slicebydate2(spy,'Date','2008-01-01','2008-10-10')
# plt.plot(t['Date'],t['High'])
a={1:[2,3,4],
  2:[3,4,5],
  3:[4,5,6]}
a=pd.DataFrame(a)
b={1:[2,8,9],
  2:[35,45,55],
  3:[45,55,65]}
b=pd.DataFrame(b)
a.join(b.set_index(1),on=1,how='inner',lsuffix='_a',rsuffix='_b')


# In[17]:


summershort=moving_average2(spy,'Adj Close',15,1,'2007-06-06','2007-10-10')
summerlong=moving_average2(spy,'Adj Close',30,1,'2007-06-06','2007-10-10')
winter=moving_average2(summershort,'roll',5,1,'2007-06-06','2007-10-10')
spring=slicebydate2(spy,'Date','2007-06-06','2007-10-11')
# plt.plot(spring['Date'],spring['Adj Close'])
plt.plot(summerlong['Date'],summerlong['roll'])
plt.plot(winter['Date'],winter['roll'])
# plt.plot(summershort['Date'],summershort['roll'])


# In[ ]:





# In[ ]:




