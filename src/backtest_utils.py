# src/backtest_utils.py

import numpy as np
import pandas as pd

def backtest_strategy_with_legs(stock_data, strike_price, option_type, position_type, start_date, end_date):
    """
    Backtests an option strategy with legs (long/short call/put) over a given stock price data.
    
    Parameters:
        stock_data (pd.DataFrame): OHLCV data for the stock
        strike_price (float): The strike price for the option
        option_type (str): 'call' or 'put'
        position_type (str): 'long' or 'short'
        start_date (str): The start date for the backtest
        end_date (str): The end date for the backtest
    
    Returns:
        pd.DataFrame: A DataFrame containing backtested option prices.
    """
    # Filter stock data for the given date range
    filtered_data = stock_data[(stock_data.index >= start_date) & (stock_data.index <= end_date)]
    
    # Generate option prices using a simple model, assuming Black-Scholes for simplicity
    option_prices = []
    for index, row in filtered_data.iterrows():
        stock_price = row['Close']
        # Simulate option price (this can be more complex based on real models)
        intrinsic_value = max(0, stock_price - strike_price) if option_type == 'call' else max(0, strike_price - stock_price)
        if position_type == 'short':
            intrinsic_value = -intrinsic_value  # Short position reverses gains/losses
        option_prices.append(intrinsic_value)
    
    # Create a DataFrame for the backtested results
    result_df = pd.DataFrame({
        'Date': filtered_data.index,
        'Option Price': option_prices
    })
    result_df.set_index('Date', inplace=True)
    
    return result_df
