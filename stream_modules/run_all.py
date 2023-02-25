import requests
import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yfin
yfin.pdr_override()
from datetime import datetime
from dateutil.relativedelta import relativedelta
import hvplot.pandas
from warnings import filterwarnings
filterwarnings("ignore")


from stream_modules.stock_tables_plugin import stock_analysis_tables
from stream_modules.monte_carlo_plugin import monte_carlo_simulation
from stream_modules.metric_results_plugin import calculate_metrics

def run(ticker, hold_unit, hold_period, req_return):
    #get table data for functions
    rolling_stock_df, bollinger_df, stock_return_df, spy_return_df, stock_spy_return_df, stock_df, spy_df = stock_analysis_tables(ticker)
    # run monte carlo simulation to test results
    monte_carlo_return_table_df, mean, lower_bound, upper_bound, avg_cum_stock_return_df, avg_cum_spy_return_df, graph_area = monte_carlo_simulation(ticker, hold_unit, hold_period, stock_df, spy_df)
    # analize all the data and provide results
    ratio_lang_final, return_lang, boiler_lang, final_lang = calculate_metrics(stock_return_df, req_return, ticker, spy_return_df, hold_unit, hold_period, avg_cum_stock_return_df, avg_cum_spy_return_df, bollinger_df)
    # # create an adaptive bollinger band graph
    # bollinger_graph = boiler_table(stock_df,ticker)
    
    #create Monte Carlo Graph
    # monte_carlo_graph = monte_carlo_return_table_df.hvplot.line(title = f"Average {hold_time} {hold_unit} Cumulative Return Monte Carlo Simulation (1,000 simulations)")
    
    return graph_area, ratio_lang_final, stock_df, boiler_lang, monte_carlo_return_table_df, return_lang, final_lang


