#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
sns.set_style('whitegrid')
import plotly
import cufflinks as cf
cf.go_offline()


# In[2]:


start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)


# ##### Creating DataFrames from Stock DATA 

# In[3]:


#BANK OF AMERICA
BAC = data.DataReader('BAC', 'yahoo', start, end)
#CITI GROUP
C = data.DataReader('C', 'yahoo', start, end)
#GOLDMAN SACHS
GS = data.DataReader('GS', 'yahoo', start, end)
#JPMORGAN CHASE
JPM = data.DataReader('JPM', 'yahoo', start, end)
#MORGAN STANLEY
MS = data.DataReader('MS', 'yahoo', start, end)
#WELLS FARGO
WFC = data.DataReader('WFC', 'yahoo', start, end)


# ##### Concatenate all DataFrames in just one

# In[4]:


tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']
bank_stocks = pd.concat([BAC,C, GS, JPM, MS, WFC], axis=1, keys=tickers)


# In[5]:


bank_stocks.columns.names = ['Bank Ticker', 'Stock Info']


# In[6]:


bank_stocks


# ##### Max close price for each banks

# In[7]:


for tick in tickers:
    print(tick, bank_stocks[tick]['Close'].max())


# In[8]:


#using .xs method to do the same task
bank_stocks.xs(key = 'Close', axis = 1, level = 'Stock Info').max()


# In[10]:


returns = pd.DataFrame()


# In[12]:


for tick in tickers:
    returns[tick + ' Return'] = bank_stocks[tick]['Close'].pct_change()


# ##### Creating a dataframe with everyday returns and plotting them.

# In[13]:


sns.pairplot(returns[1:])


# ##### Show the Day of the minimun return of each bank

# In[14]:


#Standar deviations returns from 2015
returns.loc['2015-01-01':'2015-12-31'].std()


# In[15]:


#Showing the Morgan Stanley's returns from 2015
sns.distplot(returns.loc['2015-01-01':'2015-12-31']['MS Return'], color = 'Green', bins = 50)


# In[16]:


sns.displot(returns.loc['2008-01-01':'2008-12-31']['C Return'], color = 'Red', bins = 50)


# ##### Plotting the stocks performance through the years.

# In[82]:


#Using for loop (looping through )
for tick in tickers:
    bank_stocks[tick]['Close'].plot(label = tick, figsize =(12, 4))
plt.legend()


# In[79]:


#Using the 'xs' method
bank_stocks.xs(key = 'Close', axis = 1, level = 'Stock Info').iplot()


# ##### plotting the price and the 30 day moving average of BANK OF AMERICA

# In[60]:


BAC['Close'].loc['2008-01-01':'2008-12-31'].rolling(window = 30).mean().plot(label = '30 day MA')
BAC['Close'].loc['2008-01-01':'2008-12-31'].plot(label = 'BAC PRICES', figsize= (15, 7))
plt.legend()


# In[63]:


sns.heatmap(bank_stocks.xs(key = 'Close', axis = 1, level = 'Stock Info').corr(), annot = True)


# In[64]:


sns.clustermap(bank_stocks.xs(key = 'Close', axis = 1, level = 'Stock Info').corr(), annot = True)


# In[65]:


close_corr = bank_stocks.xs(key = 'Close', axis = 1, level = 'Stock Info').corr()


# In[69]:


close_corr.iplot(kind = 'heatmap', colorscale = 'rdylbu')


# ##### Plotting BANK OF AMERICA graph with candlestick

# In[75]:


bac_2015 = BAC[['Open', 'High', 'Low', 'Close']].loc['2015-01-01':'2016-01-01']


# In[76]:


bac_2015.iplot(kind = 'candle')


# ##### Showing the price and the moving averages of Morgan Stanley

# In[83]:


MS['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study = 'ema', periods = [13, 21, 50])


# ##### Using bollinger bands in BAC

# In[84]:


BAC['Close'].loc['2015-01-01':'2016-01-01'].ta_plot(study = 'boll')


# In[ ]:




