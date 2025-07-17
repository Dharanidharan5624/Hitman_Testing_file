import yfinance as yf
import mysql.connector
import numpy as np

# Index data (valid Yahoo Finance tickers only)
indices = {
    "Dow Jones": "^DJI",
    "Russell 2000": "^RUT",
    "S&P 500": "^GSPC",
    "CBOE Volatility Index": "^VIX"
}

# Fetch index data using yfinance
def fetch_index_data(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2d")  # Use 2 days to handle weekends/holidays
    data = data.dropna(subset=["Open", "Close"])  # Remove rows with NaN values

    if data.empty:
        print(f"📭 No valid data returned for {symbol}")
        return None, None

    # Use the last available row (most recent complete data)
    close_price = data['Close'].iloc[-1]
    open_price = data['Open'].iloc[-1]

    print(f"🧾 Raw Data for {symbol} → Open: {open_price}, Close: {close_price}")

    # Check for zero open (division issue)
    if open_price == 0:
        print(f"⚠️  Open price is zero for {symbol}")
        return None, None

    percent_change = ((close_price - open_price) / open_price) * 100

    # Avoid NaN or Inf values
    if np.isnan(percent_change) or np.isinf(percent_change):
        print(f"⚠️  Invalid percent change for {symbol}")
        return None, None

    # Convert to native Python float
    return float(round(close_price, 2)), float(round(percent_change, 2))

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123',
    database='hitman_edgev_1'
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS he_index_data (
    symbol VARCHAR(10) PRIMARY KEY,
    index_name VARCHAR(50),
    close_price DECIMAL(10,2),
    percent_change DECIMAL(6,2)
)
""")

# Fetch and insert data
for name, symbol in indices.items():
    close_price, percent_change = fetch_index_data(symbol)
    
    if close_price is not None:
        query = """
        INSERT INTO he_index_data (index_name, symbol, close_price, percent_change)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            index_name = VALUES(index_name),
            close_price = VALUES(close_price),
            percent_change = VALUES(percent_change)
        """
        cursor.execute(query, (name, symbol, close_price, percent_change))
        print(f"✅ Inserted: {name} ({symbol}) → Close: {close_price}, Change: {percent_change}%")
    else:
        print(f"⚠️  Skipped: {name} ({symbol}) – Invalid or missing data")

# Commit and close connection
conn.commit()
cursor.close()
conn.close()
