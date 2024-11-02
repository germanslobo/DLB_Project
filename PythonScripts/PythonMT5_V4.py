import MetaTrader5 as mt5
import pandas as pd
import datetime

# Initialize MT5 connection
if not mt5.initialize():
    print("Failed to initialize MT5")
    mt5.shutdown()
else:
    # Prompt user for symbol input
    symbol = input("Enter the symbol (e.g., EURUSD): ").strip().upper()
    
    # Define other parameters
    timeframe = mt5.TIMEFRAME_D1  # Daily timeframe
    period_ma = 14
    period_rsi = 14
    today = datetime.datetime.now()
    start_date = today - datetime.timedelta(days=365)  # 1 year ago

    # Fetch OHLC data for the last year
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, today)
    if rates is None or len(rates) == 0:
        print(f"Failed to retrieve data for {symbol}. Please check the symbol and try again.")
        mt5.shutdown()
    else:
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert time to datetime
        df = df[['time', 'open', 'high', 'low', 'close']]  # Keep only relevant columns

        # Calculate MA (Moving Average) and RSI (Relative Strength Index)
        df['MA_14'] = df['close'].rolling(window=period_ma).mean()
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period_rsi).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period_rsi).mean()
        rs = gain / loss
        df['RSI_14'] = 100 - (100 / (1 + rs))

        # Add the symbol name as a column
        df.insert(0, 'symbol', symbol)

        # Save to CSV
        filename = f'{symbol}_daily_data_with_indicators.csv'
        df.to_csv(filename, index=False)
        print(f"Data saved successfully to '{filename}'")

    # Shutdown MT5 connection
    mt5.shutdown()
