**Black Scholes Intuition Tool**

This tool provides an intuitive way to explore option pricing using the Black-Scholes model. It is designed to help users understand how different parameters (such as stock price, volatility, time to expiry, etc.) affect option prices, Greeks, PnL, and price heatmaps.

**Features**

Single Point in Time: Provides a snapshot of an option’s price, Greeks, PnL, and a heatmap based on user-defined parameters.

Visualizing Over Time: Allows users to input a stock ticker and visualize how the option price evolves over a date range, along with the Greeks.


**Technologies Used:**

Streamlit: For creating the user interface.
Altair: For plotting stock and option price charts.
Matplotlib & Seaborn: For generating option price heatmaps.
Pandas: For handling stock data and time series.
Numpy: For numerical operations in Black-Scholes calculations.


**Installation**

Clone the repository:

git clone https://github.com/YourUsername/ProjectOptionPricer.git
cd ProjectOptionPricer


Create a virtual environment (optional but recommended):

python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt

Run the app:

streamlit run app.py



**How to Use:**

1. Single Point in Time

Adjust Pricing Inputs: You can adjust the stock price, strike price, volatility, risk-free rate, and time to expiry to see how they impact the option price.

Option Greeks: Displays the Greeks (Delta, Gamma, Theta, Vega, and Rho) to provide insight into the sensitivities of the option price.

PnL Calculator: Shows the profit and loss based on the current option price and your purchase price.

Option Price Heatmap: A heatmap that visualizes option prices for a range of stock prices and volatilities.


2. Visualizing Over Time

Stock Price Visualization: Enter a stock ticker and date range to see historical stock prices.

Option Price Visualization: See how the option price and Greeks evolve over the selected time range.


**Folder Structure**


ProjectOptionPricer/
│
├── src/
│   ├── data.py               # Fetches stock data from an API
│   ├── greeks.py             # Calculates option Greeks (Delta, Gamma, etc.)
│   ├── option_pricer.py      # Implements the Black-Scholes pricing model
│   ├── pnl.py                # Calculates profit and loss (PnL)
│   ├── strategies.py         # Implements option strategies (not used)
│   └── testing.py            # For testing (if applicable)
│
├── app.py                    # Main application file for Streamlit
├── requirements.txt          # Lists the required packages and dependencies
└── README.md                 # Project overview (this file)



**To-Do:**

Add more option strategies to the app.
Implement additional visualizations for deeper analysis.
