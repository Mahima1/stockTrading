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


'''
import time
zz=time.time()
a=spy['Adj Close']
for i in range(2516):
    a.iloc[i]/a.iloc[0]
timedif=time.time()-zz
print ("in for loop: ",timedif)

xx=time.time()
y=google['Adj Close']
y/y.iloc[0]
timediff=time.time()-xx
print ("pandas: ",timediff)

print(timedif/timediff)
'''


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
    #return temp
slicebydate(apple,'Adj Close','Date','2017-01-01','2017-05-30')


# In[8]:


#pd.to_datetime(1,origin=datetime.date(2017,5,2),unit='D')
    #temp[dfcol+' predicted']=temp.rolling(window)[dfcol].mean()
    
    #temp[dfcol+' new']=temp[dfcol+' new'].shift(1)
    #temp=temp.fillna(0)
    #temp[dfcol]=temp[dfcol]+temp[dfcol+' new']
       # print(temp['new ewm'].tail(100))


import datetime
def moving_average(df,dfcol,window,days):
    temp=pd.DataFrame()
    temp2=pd.DataFrame()
    
    temp[dfcol]=df[dfcol][::-1][:500]
    temp['Date']=df['Date'][::-1][:500]
    temp=temp[::-1]
    
    lastdate=df['Date'].iloc[-1]
    temp2['Date']=pd.date_range(start=pd.to_datetime(1,origin=lastdate,unit='D'),end=pd.to_datetime(days,origin=lastdate,unit='D'))
    temp=temp.append(temp2,ignore_index=True)
    temp['new roll']=temp.rolling(window, min_periods = 1)[dfcol].mean()
    temp['new ewm']=temp.ewm(com=3)[dfcol].mean()
    temp['std']=temp.rolling(window, min_periods = 1)[dfcol].std()
    temp['upper band']=temp['new roll']+(2*temp['std'])
    temp['lower band']=temp['new roll']-(2*temp['std'])

    plt.plot(temp['Date'],temp['new roll'])
    #plt.plot(df['Date'][2480:],df[dfcol][2480:])
    #plt.plot(temp['Date'],temp['new ewm'])
    #plt.plot(temp['Date'],temp['upper band'])
    #plt.plot(temp['Date'],temp['lower band'])

moving_average(apple,'Adj Close',50,10)


# In[9]:


import mpl_finance as candle
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime as datetime
quotes=pd.DataFrame()
'''
a=pd.DataFrame()
a=spy[['Date','Open','High','Low','Close']][:100]
a['Date'] = pd.to_datetime(a['Date'])
a["Date"] = a["Date"].apply(mdates.date2num)
quotes=a[['Date','Open','High','Low','Close']].copy()
fig,ax=plt.subplots()
#candle.candlestick2_ohlc(ax,quotes['Open'],quotes['High'],quotes['Low'],quotes['Close'])
candle.candlestick_ohlc(ax,quotes.values)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
'''
quotes=spy[['Date','Open','High','Low','Close']][spy['Date']<'2008-05-05']
fig, ax = plt.subplots()
candle.candlestick2_ohlc(ax,quotes['Open'],quotes['High'],quotes['Low'],quotes['Close'],width=0.6)

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
fig.tight_layout()

plt.plot()
moving_average(spy,'Adj Close',15,100)
moving_average(spy,'Adj Close',100,100)




