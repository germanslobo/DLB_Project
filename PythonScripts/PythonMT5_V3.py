import MetaTrader5 as mt5

# Initialize the connection to MT5
if not mt5.initialize():
    print("Failed to initialize MetaTrader5")
    mt5.shutdown()
else:
    symbol = "BTCUSD" 
    
    # Check if the symbol exists and is available
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"{symbol} not found, please check symbol name.")
        mt5.shutdown()
    elif not symbol_info.visible:
        # Try to make the symbol visible in Market Watch
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to select {symbol}, please check symbol availability.")
            mt5.shutdown()
    else:
        # Fetch the latest ask price
        price = mt5.symbol_info_tick(symbol).ask
        lot = 0.01  # Smaller lot size for testing

        # Define the buy order request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "deviation": 20,  # Increased deviation for more flexibility
            "magic": 234000,
            "comment": "Python Buy Order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # Send the buy order request
        result = mt5.order_send(request)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Buy order executed successfully! Order details: {result}")
        else:
            print(f"Buy order failed. Error code: {result.retcode}")
    
    # Shutdown the connection
    mt5.shutdown()
