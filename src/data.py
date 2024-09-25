import yfinance as yf
import pandas as pd

def get_stock_data(ticker, start, end):
    """
    Fetches historical stock data using yfinance.

    Parameters:
    ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple).
    start (str): The start date for the data (format: 'YYYY-MM-DD').
    end (str): The end date for the data (format: 'YYYY-MM-DD').

    Returns:
    DataFrame: A pandas DataFrame with historical stock data.
    """
    data = yf.download(ticker, start=start, end=end)
    data = data.reset_index()
    return data
