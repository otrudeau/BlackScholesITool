import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import base64
from src.option_pricer import black_scholes
from src.greeks import option_greeks
from src.pnl import pnl
from src.strategies import single_leg_strategy, multi_leg_strategy
from src.data import get_stock_data

# Function to load an image and convert to base64 for embedding
def load_image_as_link(image_path, link_url):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return f'<a href="{link_url}" target="_blank"><img src="data:image/png;base64,{encoded_image}" width="30"></a>'

# Load LinkedIn logo and link
linkedin_logo = load_image_as_link("src/linkedin_logo.png", "https://www.linkedin.com/in/otrudeau")

# Streamlit page configuration
st.set_page_config(page_title="Black-Scholes Intuition Tool", layout="wide")

# Banner with LinkedIn and name
st.markdown(
    """
    <div style="display:flex; align-items:center; justify-content:start;">
        <h2 style="font-size: 36px;">Black-Scholes Intuition Tool</h2>
    </div>
    <div style="display:flex; align-items:center; justify-content:start; margin-top: 10px;">
        <span style="font-size: 16px; font-weight: bold; margin-right: 10px;">Created by:</span>
        <img src='data:image/png;base64,{}' class='img-fluid' width=25 height=25 style="margin-right: 10px"/>
        <a href="https://www.linkedin.com/in/otrudeau" style="font-size: 16px; font-weight: bold; text-decoration:none;">Olivier Trudeau</a>
    </div>
    """.format(encoded_image), unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2 = st.tabs(["Single Point in Time", "Over Time"])

# ----- TAB 1: Single Point in Time -----
with tab1:
    st.markdown("### 🔧 **Pricing Inputs**")

    # Inputs for option pricing parameters
    col1, col2 = st.columns(2)
    with col1:
        S = st.slider('📈 Stock Price (S)', 0, 150, 100, key="price_single")
        K = st.slider('🔑 Strike Price (K)', 0, 150, 100, key="strike_single")
    with col2:
        T = st.slider('⏳ Time to Expiry (Years)', 0.0, 5.0, 1.0, key="time_single")
        r = st.slider('📉 Risk-Free Rate (r)', 0.0, 0.1, 0.05, key="rate_single")

    volatility = st.slider('🌪️ Volatility (σ)', 0.0, 1.0, 0.2, key="volatility_single")
    option_type = st.selectbox('Option Type', ['call', 'put'], key="option_single")

    # Calculate current option price for the user-input stock price
    current_price = black_scholes(S, K, T, r, volatility, option_type)
    st.markdown("### 📈 **Current Option Price**")
    st.info(f"Current {option_type.capitalize()} Price: **{current_price:.2f}**")

    # PnL calculation
    purchase_price = st.number_input('💰 Option Purchase Price', value=10.0, key="purchase_price")
    pnl_value = pnl(purchase_price, current_price, option_type)
    st.markdown("### 📉 **PnL (Profit and Loss)**")
    st.success(f"PnL: **{pnl_value:.2f}**")

    # Greeks calculation
    greeks = option_greeks(S, K, T, r, volatility, option_type)
    st.markdown("### ⚙️ **Greeks**")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Delta (Δ):** {greeks['Delta']:.4f}")
        st.caption("Delta represents the change in option price with a $1 move in the stock price.")
        st.info(f"**Gamma (Γ):** {greeks['Gamma']:.4f}")
        st.caption("Gamma measures the rate of change of Delta.")
    with col2:
        st.info(f"**Theta (Θ):** {greeks['Theta']:.4f}")
        st.caption("Theta represents time decay.")
        st.info(f"**Vega (V):** {greeks['Vega']:.4f}")
        st.caption("Vega represents sensitivity to volatility.")
        st.info(f"**Rho (ρ):** {greeks['Rho']:.4f}")
        st.caption("Rho measures sensitivity to interest rates.")

    # Heatmap for option prices based on volatility and stock price
    st.markdown("### 🌡️ **Option Price Heatmap**")
    vol_range = np.arange(0.00, 1.0, 0.05)
    price_range = np.linspace(10, 150, 20)
    heatmap_data = np.zeros((len(vol_range), len(price_range)))

    for i, vol in enumerate(vol_range):
        for j, price in enumerate(price_range):
            heatmap_data[i, j] = black_scholes(price, K, T, r, vol, option_type)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", xticklabels=np.round(price_range, 2), 
                yticklabels=np.round(vol_range, 2), cmap="coolwarm", ax=ax, annot_kws={"size": 7})
    ax.set_xlabel('Stock Price')
    ax.set_ylabel('Volatility')
    ax.set_title(f'{option_type.capitalize()} Price Heatmap')
    st.pyplot(fig)

# ----- TAB 2: Over Time -----
with tab2:
    st.markdown("### 🪛 **Pricing Inputs**")
    col5, col6 = st.columns(2)
    with col5:
        start_date = st.date_input("Select Start Date", value=pd.to_datetime("2020-01-01"))
    with col6:
        end_date = st.date_input("Select End Date", value=pd.to_datetime("2023-01-01"))

    ticker_viz = st.text_input('Enter Stock Ticker (e.g., AAPL):', value="AAPL", key="ticker_viz")
    col1, col2 = st.columns(2)
    with col1:
        K_viz = st.slider('🔑 Strike Price (K)', 50, 150, 100, key="strike_viz")
        r_viz = st.slider('📉 Risk-Free Rate (r)', 0.0, 0.1, 0.05, key="rate_viz")
    with col2:
        T_viz = st.slider('⏳ Time to Expiry (Years)', 0.1, 5.0, 1.0, key="time_viz")
        volatility_viz = st.slider('🌪️ Volatility (σ)', 0.1, 1.0, 0.2, key="volatility_viz")

    option_type_viz = st.selectbox('Option Type', ['call', 'put'], key="option_type_viz")

    # Fetch stock data based on ticker and date range
    stock_data = get_stock_data(ticker_viz, start=start_date, end=end_date)
    if not pd.api.types.is_datetime64_any_dtype(stock_data.index):
        stock_data.index = pd.date_range(start=start_date, end=end_date, periods=len(stock_data))
    stock_data['Date'] = stock_data.index.strftime('%Y-%m-%d')
    stock_data.set_index('Date', inplace=True)

    st.markdown(f"### 📊 **{ticker_viz.upper()} Stock Price**")
    stock_chart = alt.Chart(stock_data.reset_index()).mark_line().encode(
        x=alt.X('Date:T', axis=alt.Axis(labelAngle=-45)),
        y='Close',
        tooltip=['Date', 'Close']
    ).properties(height=400)
    st.altair_chart(stock_chart, use_container_width=True)

    # Calculate option price for each day
    option_prices = []
    greeks_df = []
    for stock_price in stock_data['Close']:
        option_price = black_scholes(stock_price, K_viz, T_viz, r_viz, volatility_viz, option_type_viz)
        option_prices.append(option_price)
        greeks = option_greeks(stock_price, K_viz, T_viz, r_viz, volatility_viz, option_type_viz)
        greeks_df.append(greeks)

    st.markdown(f"### 📈 **{ticker_viz.upper()} Option Price**")
    option_price_df = pd.DataFrame({
        'Date': stock_data.index,
        'Option Price': option_prices,
        'Delta': [g['Delta'] for g in greeks_df],
        'Gamma': [g['Gamma'] for g in greeks_df],
        'Theta': [g['Theta'] for g in greeks_df],
        'Vega': [g['Vega'] for g in greeks_df],
        'Rho': [g['Rho'] for g in greeks_df]
    }).set_index('Date')

    option_chart = alt.Chart(option_price_df.reset_index()).mark_line().encode(
        x=alt.X('Date:T', axis=alt.Axis(labelAngle=-45)),
        y='Option Price',
        tooltip=['Date', 'Option Price', 'Delta', 'Gamma', 'Theta', 'Vega', 'Rho']
    ).properties(height=400)
    st.altair_chart(option_chart, use_container_width=True)
