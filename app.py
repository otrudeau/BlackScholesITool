import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from PIL import Image
import base64
import io

# Import custom modules for calculations
from src.option_pricer import black_scholes
from src.greeks import option_greeks
from src.pnl import pnl
from src.strategies import single_leg_strategy, multi_leg_strategy
from src.data import get_stock_data

# Set Streamlit page configuration with automatic dark mode
st.set_page_config(page_title="Black-Scholes Intuition Tool", layout="wide", initial_sidebar_state="collapsed")

# Load LinkedIn logo
linkedin_logo_path = "src/linkedin_logo.png"
linkedin_logo = Image.open(linkedin_logo_path)
buffered = io.BytesIO()
linkedin_logo.save(buffered, format="PNG")
encoded_logo = base64.b64encode(buffered.getvalue()).decode()

# Custom CSS to adjust theme dynamically for fonts and the heatmap
st.markdown(f"""
    <style>
    html[theme="dark"] {{
        --primary-color: white;
        --secondary-color: #e0e0e0;
        --heatmap-bg-color: transparent;
        --legend-bg-color: white;
    }}
    html[theme="light"] {{
        --primary-color: black;
        --secondary-color: #6e6e6e;
        --heatmap-bg-color: transparent;
        --legend-bg-color: black;
    }}

    .header {{
        font-size: 36px;
        font-weight: bold;
        color: var(--primary-color);
    }}
    .created-by {{
        font-size: 16px;
        color: var(--secondary-color);
        margin-bottom: 10px;
    }}
    .name-link {{
        font-size: 20px;
        color: #1DA1F2;
        text-decoration: none;
        padding-left: 10px;
    }}
    .linkedin-logo {{
        width: 25px;
        vertical-align: middle;
        margin-left: 5px;
    }}
    .explanation-box {{
        background-color: rgba(255, 165, 0, 0.1);
        border: 2px solid orange;
        padding: 15px;
        color: var(--primary-color);
        border-radius: 5px;
        margin-bottom: 20px;
    }}
    </style>
    <div class="header">Black-Scholes Intuition Tool</div>
    <div class="created-by">Created by:</div>
    <img src='data:image/png;base64,{encoded_logo}' class='linkedin-logo'><a href="https://www.linkedin.com/in/otrudeau" class="name-link">Olivier Trudeau</a><br><br>
    """, unsafe_allow_html=True)

# Tabs for Single Point in Time and Over Time
tab1, tab2 = st.tabs(["Single Point in Time", "Over Time"])

# ----- TAB 1: Single Point in Time -----
with tab1:
    st.markdown(
        '''
        <div class="explanation-box">
            Adjusting parameters will dynamically recalculate the option price, PnL, greeks, and the heatmap below, helping you understand how each factor affects option pricing.
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    st.markdown("### 🔧 **Pricing Inputs**")
    
    col1, col2 = st.columns(2)
    with col1:
        S = st.slider('📈 Stock Price (S)', 0, 150, 100, key="price_single")
        K = st.slider('🔑 Strike Price (K)', 0, 150, 100, key="strike_single")
    with col2:
        T = st.slider('⏳ Time to Expiry (Years)', 0.0, 5.0, 1.0, key="time_single")
        r = st.slider('📉 Risk-Free Rate (r)', 0.0, 0.1, 0.05, key="rate_single")

    volatility = st.slider('🌪️ Volatility (σ)', 0.0, 1.0, 0.2, key="volatility_single")
    option_type = st.selectbox('Option Type', ['call', 'put'], key="option_single")

    st.markdown("<br>", unsafe_allow_html=True)

    # Calculate current option price
    current_price = black_scholes(S, K, T, r, volatility, option_type)
    st.markdown("### 📈 **Current Option Price**")
    st.info(f"Current {option_type.capitalize()} Price: **{current_price:.2f}**")

    purchase_price = st.number_input('💰 Option Purchase Price', value=10.0, key="purchase_price")
    pnl_value = pnl(purchase_price, current_price, option_type)
    st.markdown("### 📉 **PnL (Profit and Loss)**")
    st.success(f"PnL: **{pnl_value:.2f}**")

    st.markdown("<br>", unsafe_allow_html=True)

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
        st.caption("Rho measures the sensitivity of the option price to changes in interest rates.")

    # Heatmap Section
    st.markdown("### 🌡️ **Option Price Heatmap**")
    vol_range = np.arange(0.00, 1.0, 0.05)
    price_range = np.linspace(10, 150, 20)
    heatmap_data = np.zeros((len(vol_range), len(price_range)))

    for i, vol in enumerate(vol_range):
        for j, price in enumerate(price_range):
            heatmap_data[i, j] = black_scholes(price, K, T, r, vol, option_type)

       # Create the heatmap
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.heatmap(heatmap_data, annot=True, fmt=".2f", xticklabels=np.round(price_range, 2), 
                yticklabels=np.round(vol_range, 2), cmap="coolwarm", ax=ax, annot_kws={"size": 7})

    # Set the heatmap background and text colors
    ax.set_facecolor((0, 0, 0, 0))  # Transparent-like effect with RGBA
    fig.patch.set_facecolor((0, 0, 0, 0))  # Transparent figure background with RGBA

    # Color for ticks and labels dynamically based on theme
    tick_color = 'black' if st.get_option('theme.base') == 'light' else 'white'
    
    # Adjust tick colors on X and Y axes
    plt.xticks(color=tick_color)  # Dynamic text color for X-axis
    plt.yticks(color=tick_color)  # Dynamic text color for Y-axis

    # Set X and Y axis labels and title
    ax.set_xlabel('Stock Price', color=tick_color)
    ax.set_ylabel('Volatility', color=tick_color)
    ax.set_title(f'{option_type.capitalize()} Price Heatmap', color=tick_color)

    # Set colorbar and adjust its label and ticks color
    cbar = ax.collections[0].colorbar
    cbar.ax.yaxis.set_tick_params(color=tick_color)  # Set color for the colorbar ticks
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=tick_color)  # Set color for colorbar labels

    st.pyplot(fig)

# ----- TAB 2: Visualizing Over Time -----
with tab2:
    # Explanation Text in a White Box with an Orangey Border
    st.markdown(
        f'''
        <style>
        .explanation-box {{
            background-color: rgba(255, 165, 0, 0.1);
            border: 2px solid orange;
            padding: 15px;
            color: var(--primary-color);
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        </style>
        <div class="explanation-box">
            These inputs will impact the Option Price graph below. Adjusting parameters will show how option pricing evolves.
        </div>
        ''',
        unsafe_allow_html=True
    )
    
    st.markdown(f"### 🪛 **Pricing Inputs**", unsafe_allow_html=True)

    # Date range for stock data visualization
    col5, col6 = st.columns(2)
    with col5:
        start_date = st.date_input("Select Start Date", value=pd.to_datetime("2020-01-01"))
    with col6:
        end_date = st.date_input("Select End Date", value=pd.to_datetime("2023-01-01"))

    # Inputs for option pricing parameters (Visualizing Over Time)
    ticker_viz = st.text_input('Enter Stock Ticker (e.g., AAPL):', value="AAPL", key="ticker_viz")
    col1, col2 = st.columns(2)
    with col1:
        K_viz = st.slider('🔑 Strike Price (K)', 50.0, 150.0, 100.0, key="strike_viz")
        r_viz = st.slider('📉 Risk-Free Rate (r)', 0.0, 0.1, 0.05, key="rate_viz")
    with col2:
        T_viz = st.slider('⏳ Time to Expiry (Years)', 0.1, 5.0, 1.0, key="time_viz")
        volatility_viz = st.slider('🌪️ Volatility (σ)', 0.1, 1.0, 0.2, key="volatility_viz")

    option_type_viz = st.selectbox('Option Type', ['call', 'put'], key="option_type_viz")

    # Fetch stock data based on ticker and date range
    stock_data = get_stock_data(ticker_viz, start=start_date, end=end_date)

    # Check if the index is not already a DateTimeIndex and convert if necessary
    if not pd.api.types.is_datetime64_any_dtype(stock_data.index):
        stock_data.index = pd.date_range(start=start_date, end=end_date, periods=len(stock_data))

    # Convert DateTimeIndex to strings for proper labeling in Streamlit's line_chart
    stock_data['Date'] = stock_data.index.strftime('%Y-%m-%d')
    stock_data.set_index('Date', inplace=True)

    # Display Stock Price Chart using Altair
    st.markdown(f"### 📊 **{ticker_viz.upper()} Stock Price**", unsafe_allow_html=True)
    stock_chart = alt.Chart(stock_data.reset_index()).mark_line().encode(
        x=alt.X('Date:T', axis=alt.Axis(labelAngle=-45)),
        y='Close',
        tooltip=['Date', 'Close']
    ).properties(
        height=400
    )

    st.altair_chart(stock_chart, use_container_width=True)  # Full width

    # Add heading for option price chart
    st.markdown(f"### 📈 **{ticker_viz.upper()} Option Price**", unsafe_allow_html=True)

    # Calculate option price for each day
    option_prices = []
    greeks_df = []  # Placeholder for storing Greeks for each date
    for stock_price in stock_data['Close']:
        option_price = black_scholes(stock_price, K_viz, T_viz, r_viz, volatility_viz, option_type_viz)
        option_prices.append(option_price)
        # Compute Greeks
        greeks = option_greeks(stock_price, K_viz, T_viz, r_viz, volatility_viz, option_type_viz)
        greeks_df.append(greeks)
        
    # Display Option Price Chart using Altair
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
    ).properties(
        height=400
    )

    st.altair_chart(option_chart, use_container_width=True)  # Full width
