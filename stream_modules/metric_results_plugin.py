import pandas as pd
import numpy as np
import hvplot.pandas
from pathlib import Path

def calculate_metrics (stock_return_df, required_return, ticker, bench_return_df, time_period, time_numeric, monte_stock_df, monte_bench_df, boiler_band_df):
    #remove accidental NAs
    stock_return_df=stock_return_df.dropna()
    bench_return_df=bench_return_df.dropna()
    #calculate normal standard deviation for the stock sharpe ratio
    stock_norm_sdv = float(stock_return_df.std())*(252**(1/2))
    #calcualte averge return for sharpe ratio
    stock_mean_return = float(stock_return_df.mean())*252
    #calculate standard deviation of negative returns for sortino ratio
    stock_negative_returns = stock_return_df[stock_return_df<0]
    stock_neg_sdv = float(stock_negative_returns.std())*(252**(1/2))
    #convert the annual requied return into a daily return using a geometric method
    required_daily = (required_return/100)
    #calculate the sharpe and sortino ratios
    stock_sharpe_ratio = round((stock_mean_return - required_daily)/stock_norm_sdv,4)
    stock_sortino_ratio = round((stock_mean_return - required_daily)/stock_neg_sdv,4)
    
    #calculate normal standard deviation for the market sharpe ratio
    bench_norm_sdv = float(bench_return_df.std())*(252**(1/2))
    #calcualte averge return for sharpe ratio
    bench_mean_return = float(bench_return_df.mean())*252
    #calculate standard deviation of negative returns for sortino ratio
    bench_negative_returns = bench_return_df[bench_return_df<0]
    bench_neg_sdv = float(bench_negative_returns.std())*(252**(1/2))
    #calculate the sharpe and sortino ratios
    bench_sharpe_ratio = round((bench_mean_return - required_daily)/bench_norm_sdv,4)
    bench_sortino_ratio = round((bench_mean_return - required_daily)/bench_neg_sdv,4)
    
    # get the final boilder band price targets
    stock_price = float(round(boiler_band_df.iloc[-1,0],2))
    upper_price = float(round(boiler_band_df.iloc[-1,1],2))
    lower_price = float(round(boiler_band_df.iloc[-1,2],2))
    
    #calculate the annulized return rate of the monte carlo simulations
    monte_stock_return = float(monte_stock_df.iloc[-1])
    monte_bench_return = float(monte_bench_df.iloc[-1])
    
    if time_period == "days":
        monte_stock_annual = round((monte_stock_return**(252/time_numeric))*100-100,2)
        monte_bench_annual = round((monte_bench_return**(252/time_numeric))*100-100,2)
    elif time_period == "months":
        monte_stock_annual = round((monte_stock_return**(12/time_numeric))*100-100,2)
        monte_bench_annual = round((monte_bench_return**(12/time_numeric))*100-100,2)
    elif time_period == "years":
        monte_stock_annual = round((monte_stock_return**(1/time_numeric))*100-100,2)
        monte_bench_annual = round((monte_bench_return**(1/time_numeric))*100-100,2)
   
    # results depending sortino results language
    if stock_sharpe_ratio<=0.00:
        ratio_lang = "negative. This indicates that the average security return did not exceed the return requirements. In this case Both the Sharpe and Sortino ratio are not stable judges of performance."
    elif stock_sortino_ratio>stock_sharpe_ratio:
        ratio_lang = f"less than the Sortino Ratio ({stock_sortino_ratio}). This means that security has more upside volatility potential."
    else:
        ratio_lang = f"greater than the Sortino Ratio ({stock_sortino_ratio}): This means that the security has more downside volatility potential."

    # Did the security meet the expected annual return
    if monte_stock_annual >= required_return:
        return_lang = f"According to the monte carlo simulation {ticker} is expected to meet the required rate of return (Stock Return: {monte_stock_annual}%, Required Rate: {required_return}%)."
    elif (monte_stock_annual <= required_return) and (monte_bench_annual >= required_return):
        return_lang = f"According to the monte carlo simulation {ticker} is noted expected to meet the required rate of return (Stock Annual Return: {monte_stock_annual}%, Required Rate: {required_return}%). However, the general market is able to meet the return requirements (Market Return: {monte_bench_annual}%)."
    else:
        return_lang = f"According to the monte carlo simulation neither {ticker} nor the S&P 500 are able to meet the your return requirements (Stock Return: {monte_stock_annual}%, Market Return: {monte_bench_annual}%, Required Rate: {required_return}%)."
    
    #boiler band results
    if stock_price>upper_price:
        boiler_lang = f"The current stock price for {ticker} (${stock_price}) is greater than the upper boiler band (${upper_price}). This may indicate that the security is currently overpurchased and that one may benefit form shorting the security."
    elif stock_price<lower_price:
        boiler_lang = f"The current stock price for {ticker} (${stock_price}) is less than the lower boiler band (${lower_price}). This may indicate that the security is currently oversold and that one may benefit form purchasing the security."
    else:
        boiler_lang = f"The stock price for {ticker} (${stock_price}) currently rests between the upper and lower boiler bands. At this point in time there is no major oppertunity to take advantage of market fluctuations."

    # stock finalized recommendation
    if (monte_stock_annual <= required_return) and (monte_bench_annual <= required_return):
        final_lang = f"Ultimately the neither {ticker} nor the S&P 500 could meet the required rate of return. It is recommended that you either research an additional security or select a more attainable return requirement."
    elif (monte_stock_annual >= required_return) and (monte_bench_annual <= required_return):
        final_lang = f"According to our monte carlo simulation {ticker} was able to meet the return requirements while the genernal market was not. As such we would recommend investing in {ticker} to meet your return goals."
    elif (monte_stock_annual <= required_return) and (monte_bench_annual >= required_return):
        final_lang = f"According to our monte carlo simulation {ticker} was unable to meet your return requirements, however the genernal market did meet the return requirements. As such we would recommend investing in the S&P 500 to meet your return goals."
    elif (monte_stock_annual >= required_return) and (monte_bench_annual >= required_return) and (bench_sortino_ratio > stock_sortino_ratio):
        final_lang = f"According to our monte carlo simulation both the market and {ticker} are able to exceed the return requirements. However, the genernal market had a higher Sortino Ratio ({bench_sortino_ratio}) than {ticker} ({stock_sortino_ratio}) indicating that it may provide a greater risk adjusted return than {ticker}."
    elif (monte_stock_annual >= required_return) and (monte_bench_annual >= required_return) and (bench_sortino_ratio < stock_sortino_ratio):
        final_lang = f"According to our monte carlo simulation both the market and {ticker} are able to exceed the return requirements. However, the {ticker} has a higher Sortino Ratio ({stock_sortino_ratio}) then the S&P 500 ({bench_sortino_ratio}) indicating that it may provide a greater risk adjusted return than the market."
    else:
        final_lang = "Sorry, we're unable to provide an recommendation at this time"

    #resutls
    ratio_lang_final = f"The Sharpe Ratio is commonly known as the reward-to-varianility ratio. It measures the excess return of a security per unit of volatility. A higher sharpe ratio indicates that a security has a supposidly higher risk adjust return. The Sortino ratio is similar however, it measures excess return per unit of downside volatility. The Sharpe Ratio ({stock_sharpe_ratio}) for {ticker} is {ratio_lang}"
    
    return ratio_lang_final, return_lang, boiler_lang, final_lang