import datetime as dt
import pandas as pd   
import numpy as np
import matplotlib.pyplot as plt

def monte_carlo_simulation(ticker, hold_unit, hold_time, stock_df, spy_df):
    
    # prepare stock data
    stock_data_selected = stock_df['Close']
    stock_data_spy = spy_df['Close']
    
    selected_stock = ticker
    # Let user input how much money he or she would like to invest
    initial_investment = 1 

    # Prepare parameters for Monte Carlo Simulation
    if hold_unit=='days':
        trading_days = hold_time
    elif hold_unit=='months':
        trading_days = hold_time*22
    else:
        trading_days = 252 * hold_time
      
    num_simulations = 1000  

    # Calculate cumulative returns and average cumulative returns for selected stock
    daily_returns_selected = stock_data_selected.pct_change().dropna().values 
    cumulative_returns_selected = np.zeros((trading_days, num_simulations))
    for i in range(num_simulations):
        daily_returns_random_selected = np.random.choice(daily_returns_selected, trading_days, replace=True)
        cumulative_returns_selected[:, i] = initial_investment * (1 + daily_returns_random_selected).cumprod(axis=0)    
  
    cumulative_returns_selected_df = pd.DataFrame(cumulative_returns_selected, columns=[f"Simulation {i}" for i in range(num_simulations)])
    average_cumulative_returns_selected_df = pd.DataFrame(
        cumulative_returns_selected_df.mean(axis=1), 
        columns=[f"Average Cumulative Returns - {selected_stock}"]
    )
 
    # Calculate cumulative returns and average cumulative returns for S&P 500
    daily_returns_spy = stock_data_spy.pct_change().dropna().values
    cumulative_returns_spy = np.zeros((trading_days, num_simulations))
    for i in range(num_simulations):
        daily_returns_random_spy = np.random.choice(daily_returns_spy, trading_days, replace=True)
        cumulative_returns_spy[:, i] = initial_investment * (1 + daily_returns_random_spy).cumprod(axis=0)    
    # Create a DataFrame of the cumulative returns
    cumulative_returns_spy_df = pd.DataFrame(cumulative_returns_spy, columns=[f"Simulation {i}" for i in range(num_simulations)])
    # Create a DataFrame of the average cumulative returns
    average_cumulative_returns_spy_df = pd.DataFrame(
        cumulative_returns_spy_df.mean(axis=1), 
        columns=["Average Cumulative Returns - SPY"]
    )

    # Create a new DataFrame to compare the average cumulative returens of the selected stock and the S&P
    monte_carlo_return_table_df = pd.concat([average_cumulative_returns_spy_df, average_cumulative_returns_selected_df], axis=1)
    avg_cum_stock_return_df = average_cumulative_returns_selected_df
    avg_cum_spy_return_df = average_cumulative_returns_spy_df

    # Prepare parameters for mean and 95% confidence interval for the histogram
    mean = np.mean(cumulative_returns_selected[-1, :])
    std = np.std(cumulative_returns_selected[-1, :])
    lower_bound = np.percentile(cumulative_returns_selected[-1, :],95)
    upper_bound = np.percentile(cumulative_returns_selected[-1, :],5)
    
    roll_mean = pd.DataFrame(cumulative_returns_selected).mean(axis=1)
    roll_std = pd.DataFrame(cumulative_returns_selected).std(axis=1)
    min_val = pd.DataFrame(cumulative_returns_selected).quantile(q=.95,axis=1,interpolation='lower')
    max_val = pd.DataFrame(cumulative_returns_selected).quantile(q=.05,axis=1,interpolation='higher')
    
    graph_area = plt.figure(figsize=(16,6))
    plt.plot(average_cumulative_returns_selected_df.index, 
             average_cumulative_returns_selected_df[f"Average Cumulative Returns - {selected_stock}"],
             color='blue',
             label = f"Cumulative {selected_stock} Returns",
             figure=graph_area)
    plt.plot(average_cumulative_returns_spy_df.index,
             average_cumulative_returns_spy_df["Average Cumulative Returns - SPY"],
             color='red',
             label = "Cumulative SPY Returns",
             figure=graph_area)
    plt.fill_between(average_cumulative_returns_selected_df.index, 
                     min_val,
                     max_val, 
                     color='blue', 
                     alpha=.2,
                     figure=graph_area)
    plt.title(f"Average {hold_time} {hold_unit} Cumulative Return Monte Carlo Simulation (1,000 simulations)", 
              fontdict=None,
              loc = 'center',
              figure=graph_area)
    plt.legend(loc='upper right')

    return monte_carlo_return_table_df, mean, lower_bound, upper_bound, avg_cum_stock_return_df, avg_cum_spy_return_df, graph_area