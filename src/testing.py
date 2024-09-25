import pandas as pd
import numpy as np

def backtest_strategy_with_legs(stock_data, strike_price, option_type, position_type, start_date, end_date):
    # Ensure the stock data index is a datetime index
    stock_data.index = pd.to_datetime(stock_data.index)
    
    # Filter data within the start and end date
    filtered_data = stock_data[(stock_data.index >= start_date) & (stock_data.index <= end_date)]
    
    # Placeholder logic for option price, replace with actual option pricing logic
    option_prices = np.random.randn(len(filtered_data)) * 10 + strike_price
    
    # Create DataFrame with Date and Option Price
    result_df = pd.DataFrame({
        'Date': filtered_data.index,
        'Option Price': option_prices
    })
    
    return result_df
