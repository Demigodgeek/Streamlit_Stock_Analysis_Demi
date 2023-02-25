# import required libraries
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from stream_modules.run_all import run
from stream_modules.stream_bollinger import boiler_table

def get_ticker_symbol(ticker):
    endpoint = "https://finance.yahoo.com/quote/" + ticker
    response = requests.get(endpoint)
    if response.status_code == 200:
        start_index = response.text.find('<title>') + len('<title>')
        end_index = response.text.find('</title>')
        full_name = response.text[start_index:end_index].split("(")[0].strip()
        return full_name
    else:
        return None

# set up streamlit page
st.set_page_config(page_title="My Webpage", page_icon="tda", layout="wide")

# create a page header
with st.container():
    st.title("Stock Analyzer & Recommendation")
    st.write("Let's see how good your investment decisions are!")

# create two columns for questionary and analysis restults
with st.container():
    st.write("---")

    col1, col2 = st.columns([1, 3], gap="medium")
    # define a variable to track if all column 1 inputs are completed
    column1_completed = False
    # column 1 used for entering inputs that will define the function
    with col1:
        st.subheader("First, let's get some information")
        ticker = st.text_input("Please enter a stock ticker").upper()
        if ticker and ticker != "SPY":
            full_name = get_ticker_symbol(ticker)
            if full_name:
                hold_unit = st.selectbox("What period do you want to hold this stock for?",('Years','Months','Days')).lower()
                hold_period = int(st.number_input(f"How many {hold_unit}?",min_value=1))
                req_return = st.number_input("What is your annualized required rate of return? (%)", min_value=0.00, format="%.2f")
                column1_completed = True
            else:
                st.warning("Please enter a valid stock symbol.")
        elif ticker == "SPY":
            st.warning("Please enter a valid stock symbol other than SPY.")
    
    # column 2 will display the results
    with col2:
        if column1_completed:
            #run the main functions and obtain all the neede variables and language
            graph_area, ratio_lang_final, stock_df, boiler_lang, monte_carlo_return_table_df, return_lang, final_lang = run(ticker,hold_unit,hold_period,req_return)
            #display ratio analysis results
            with st.container():
                st.subheader(f"{ticker} Ratio Analysis")
                st.write(f"{ratio_lang_final}")
            #display bollinger band results
            with st.container():
                st.write("---")
                #allow user to select bolling band range
                st.subheader(f"{ticker} Bollering Band Results")
                range = int(st.selectbox("Bolling Band Rolling Period",(15,30,60,90,180)))
                #run function to get new table
                bollinger_graph = boiler_table(stock_df, ticker, range)
                bollinger_graph
                st.write(f"{boiler_lang}")
            #show monte carlo simulation results
            with st.container():
                st.write("---")
                st.subheader(f"{ticker} Monte Carlo Simulation Results")
                graph_area
                st.write(f"{return_lang}")
            #show final recommendation results
            with st.container():
                st.write("---")
                st.subheader(f"{ticker} Final Recommendation")
                st.write(f"{final_lang}")
        else:
            st.info("Please fill out all the fields above to see the results.")