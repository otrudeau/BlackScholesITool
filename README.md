# Black Scholes Intuition Tool

**Version 1.0**  
**Author:** [Olivier Trudeau](https://github.com/otrudeau)

A Python-based web app built with Streamlit to help visualize option pricing, PnL, Greeks, and heatmaps for better understanding of option behavior based on the Black-Scholes model.

---

## 🚀 **Features**
- **Dynamic Option Pricing**: Calculate call/put prices based on Black-Scholes model inputs.
- **PnL Calculation**: Track the performance of an option based on the purchase price.
- **Greeks Calculation**: Real-time calculation of Delta, Gamma, Vega, Theta, and Rho.
- **Heatmap Visualization**: Visualize how option prices change with volatility and stock price.
- **Historical Data**: Fetch historical stock prices to see how option prices evolved over time.

---

## 🛠 **Tech Stack**

- **Python 3.8+**
- **Streamlit**
- **Pandas**
- **Matplotlib**
- **Seaborn**
- **Altair**

---

## 🧰 **Installation**

1. Clone the repository:
   ```bash
   git clone https://github.com/otrudeau/BlackScholesTool.git

2. Navigate to the project directory:
   ```bash
   cd BlackScholesTool
   
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

---

## 🚀 Running the Application

1. Ensure you are in the virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows

2. Run the Streamlit app:
   ```bash
   streamlit run app.py

---

## 🧠 How to Use

**Single Point in Time**: Adjust the Stock Price, Strike Price, Volatility, Risk-Free Rate, and Time to Expiry sliders to recalculate the option price, PnL, and Greeks dynamically. View the Heatmap to see how the price varies with different stock prices and volatilities.

**Visualizing Over Time**: Enter a stock ticker and adjust parameters to fetch historical stock data.
Hover over the chart to see real-time Greeks updates and track how the option price evolves.


---

## 🔮 **Future Features**
- **Multi-leg Option Strategies**: Implement predefined strategies like Iron Condor, Straddle, etc.
- **Advanced Backtesting**: Run backtests for various option strategies using historical data.
- **Interactive Tutorials**: Add step-by-step explanations for new traders to understand option pricing.

---

## 📝 **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 **Author**
**Olivier Trudeau** - [LinkedIn](https://www.linkedin.com/in/otrudeau) | [GitHub](https://github.com/otrudeau)

---

## 📫 **Contributing**

Contributions are welcome! Feel free to open a pull request or issue if you have any suggestions or improvements.

1. **Fork** the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a **Pull Request**








