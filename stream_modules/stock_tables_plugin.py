import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
from datetime import datetime
from dateutil.relativedelta import relativedelta

# The function has 5 outputs. Therefore, when you call the function, you must define 5 outputs.
# Example: rolling_stock_df, bollinger_df, stock_result_df, spy_result_df, stock_spy_return_df = stock_analysis_tables(10, 21, ticker)

def stock_analysis_tables (ticker):
    end = dt.date.today()
    start= end - dt.timedelta(days=365*10)
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')

    stock_df = pdr.get_data_yahoo(ticker, start=start_str, end=end_str)
    spy = 'SPY'
    spy_df = pdr.get_data_yahoo(spy, start=start_str, end=end_str)
    
    # Calculate the rolling mean and standard deviation
    stock_df['Rolling Mean'] = stock_df['Close'].rolling(window=30).mean()
    stock_df['Rolling Std'] = stock_df['Close'].rolling(window=30).std()
    
    # Create a new dataframe with the close price, rolling mean, and rolling standard deviation
    rolling_stock_df = stock_df[['Close', 'Rolling Mean', 'Rolling Std']]
    
    # Calculate the upper and lower Bollinger Bands
    upper_band = stock_df['Rolling Mean'] + 2 * stock_df['Rolling Std']
    lower_band = stock_df['Rolling Mean'] - 2 * stock_df['Rolling Std']
    
    # Create a new dataframe with the stock close price, upper and lower Bollinger Bands
    bollinger_df = pd.concat([stock_df['Close'], upper_band, lower_band], axis=1)
    bollinger_df.columns = ['Close', 'Upper Band', 'Lower Band']
    bollinger_df = bollinger_df.dropna()
    
    # Calculate the daily stock return
    stock_return = stock_df['Close'].pct_change()
    
    # Create a new dataframe with the stock return
    stock_return_df = pd.DataFrame(stock_return)
    stock_return_df.columns = ['Stock Return']
    
    # Calculate the daily SPY return
    spy_return = spy_df['Close'].pct_change()
    
    # Create a new dataframe with the SPY return
    spy_return_df = pd.DataFrame(spy_return)
    spy_return_df.columns = ['SPY Return']
    
    # Combine the stock return and SPY return in one dataframe
    stock_spy_return_df = pd.concat([stock_return_df, spy_return_df], axis=1)
    
    return rolling_stock_df, bollinger_df, stock_return_df, spy_return_df, stock_spy_return_df, stock_df, spy_df