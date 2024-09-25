import numpy as np
from src.option_pricer import black_scholes

# Single-leg strategy function
def single_leg_strategy(S, K, T, r, sigma, option_type, strategy):
    prices = np.linspace(S - 50, S + 50, 100)  # Stock price range for the graph
    payouts = []

    for price in prices:
        if strategy == 'long_call':
            payoff = max(price - K, 0) - black_scholes(S, K, T, r, sigma, 'call')
        elif strategy == 'long_put':
            payoff = max(K - price, 0) - black_scholes(S, K, T, r, sigma, 'put')
        elif strategy == 'short_call':
            payoff = black_scholes(S, K, T, r, sigma, 'call') - max(price - K, 0)
        elif strategy == 'short_put':
            payoff = black_scholes(S, K, T, r, sigma, 'put') - max(K - price, 0)
        elif strategy == 'covered_call':
            call_price = black_scholes(S, K, T, r, sigma, 'call')
            payoff = price - call_price  # Covered call = stock - call option
        elif strategy == 'protective_put':
            put_price = black_scholes(S, K, T, r, sigma, 'put')
            payoff = price - put_price  # Protective put = stock - put option
        elif strategy == 'cash_secured_put':
            put_price = black_scholes(S, K, T, r, sigma, 'put')
            payoff = -put_price  # You get the premium, so payoff is negative cost
        else:
            return [], [], "Strategy not found."

        payouts.append(payoff)

    return prices, payouts, f"{strategy.replace('_', ' ').title()}: Expected payoff as stock price changes."


# Multi-leg strategy function
def multi_leg_strategy(S, K1, K2, K3, K4, T, r, sigma, strategy):
    prices = np.linspace(S - 50, S + 50, 100)  # Stock price range for the graph
    payouts = []

    for price in prices:
        if strategy == 'bull_call_spread':
            # Buy call at K1, sell call at K2
            long_call = max(price - K1, 0) - black_scholes(S, K1, T, r, sigma, 'call')
            short_call = black_scholes(S, K2, T, r, sigma, 'call') - max(price - K2, 0)
            payoff = long_call + short_call

        elif strategy == 'bear_put_spread':
            # Buy put at K1, sell put at K2
            long_put = max(K1 - price, 0) - black_scholes(S, K1, T, r, sigma, 'put')
            short_put = black_scholes(S, K2, T, r, sigma, 'put') - max(K2 - price, 0)
            payoff = long_put + short_put

        elif strategy == 'iron_condor':
            # Sell call at K2, buy call at K3; sell put at K1, buy put at K4
            short_call = black_scholes(S, K2, T, r, sigma, 'call') - max(price - K2, 0)
            long_call = max(price - K3, 0) - black_scholes(S, K3, T, r, sigma, 'call')
            short_put = black_scholes(S, K1, T, r, sigma, 'put') - max(K1 - price, 0)
            long_put = max(K4 - price, 0) - black_scholes(S, K4, T, r, sigma, 'put')
            payoff = short_call + long_call + short_put + long_put

        elif strategy == 'iron_butterfly':
            # Short straddle (short call at K2, short put at K2) + long wings (buy call at K3, buy put at K1)
            short_call = black_scholes(S, K2, T, r, sigma, 'call') - max(price - K2, 0)
            short_put = black_scholes(S, K2, T, r, sigma, 'put') - max(K2 - price, 0)
            long_call = max(price - K3, 0) - black_scholes(S, K3, T, r, sigma, 'call')
            long_put = max(K1 - price, 0) - black_scholes(S, K1, T, r, sigma, 'put')
            payoff = short_call + short_put + long_call + long_put

        elif strategy == 'butterfly_spread':
            # Buy call at K1, sell 2 calls at K2, buy call at K3
            long_call_low = max(price - K1, 0) - black_scholes(S, K1, T, r, sigma, 'call')
            short_call = 2 * (black_scholes(S, K2, T, r, sigma, 'call') - max(price - K2, 0))
            long_call_high = max(price - K3, 0) - black_scholes(S, K3, T, r, sigma, 'call')
            payoff = long_call_low + short_call + long_call_high

        elif strategy == 'straddle':
            # Buy a call and a put at the same strike (K1)
            long_call = max(price - K1, 0) - black_scholes(S, K1, T, r, sigma, 'call')
            long_put = max(K1 - price, 0) - black_scholes(S, K1, T, r, sigma, 'put')
            payoff = long_call + long_put

        elif strategy == 'strangle':
            # Buy a call at K2, buy a put at K1
            long_call = max(price - K2, 0) - black_scholes(S, K2, T, r, sigma, 'call')
            long_put = max(K1 - price, 0) - black_scholes(S, K1, T, r, sigma, 'put')
            payoff = long_call + long_put

        else:
            return [], [], "Strategy not found."

        payouts.append(payoff)

    return prices, payouts, f"{strategy.replace('_', ' ').title()}: Expected payoff as stock price changes."
