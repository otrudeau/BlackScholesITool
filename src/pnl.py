def pnl(purchase_price, current_price, option_type):
    if option_type not in ['call', 'put']:
        raise ValueError("Invalid option type")

    return current_price - purchase_price if option_type == 'call' else purchase_price - current_price
