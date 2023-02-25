import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

def boiler_table(stock_df,ticker,range):
    i=range
    temp_stock_df = stock_df
    temp_stock_df['Rolling Mean'] = temp_stock_df['Close'].rolling(window=i).mean()
    temp_stock_df['Rolling Std'] = temp_stock_df['Close'].rolling(window=i).std()
        
    # Create a new dataframe with the close price, rolling mean, and rolling standard deviation
    rolling_stock_df = stock_df[['Close', 'Rolling Mean', 'Rolling Std']]
    
    # Calculate the upper and lower Bollinger Bands
    upper_band = stock_df['Rolling Mean'] + 2 * stock_df['Rolling Std']
    lower_band = stock_df['Rolling Mean'] - 2 * stock_df['Rolling Std']
        
    temp_boil_df = pd.concat([stock_df['Close'], upper_band, lower_band], axis=1)
    temp_boil_df.columns = ['Close', 'Upper Band', 'Lower Band']
    end = dt.date.today()
    start= end - dt.timedelta(days=60)
    temp_boil_df = temp_boil_df[start:end]
    bolling_graph_data = temp_boil_df

    bolling_graph = plt.figure(figsize=(16,4))
    plt.plot(bolling_graph_data['Close'],
             color='blue',
             label = "Close Price",
             figure=bolling_graph)
    plt.plot(bolling_graph_data['Upper Band'],
             color='red',
             label = "Upper Bollinger Band",
             figure=bolling_graph)
    plt.plot(bolling_graph_data['Lower Band'],
             color='green',
             label = "Lower Bollinger Band",
             figure=bolling_graph)
    plt.title(f'{range} Day Rolling Bollinger Bands For {ticker}', 
            fontdict=None,
            loc = 'center',
            figure=bolling_graph)
    plt.legend(loc='lower right')
        
    return bolling_graph