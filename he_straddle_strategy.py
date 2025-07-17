from pytz import timezone
from datetime import datetime, timedelta
import yfinance as yf
import time
import mysql.connector
import numpy as np
from ib_insync import *

# === CONFIG ===
eastern = timezone("US/Eastern")
symbols = ["SPY", "AAPL"]
start_time = datetime.now(eastern)
end_time = start_time + timedelta(minutes=10)

print(f"Script will run daily between {start_time.strftime('%H:%M:%S')} and {end_time.strftime('%H:%M:%S')} US/Eastern Time.\n")

# === IBKR Setup ===
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# === DB STORE FUNCTION ===
def store_data_in_db(data):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="123", database="hitman")
        cursor = conn.cursor()
        sql = """INSERT INTO options_trading (stock_symbol, stock_price, call_premium, put_premium)
                 VALUES (%s, %s, %s, %s)"""
        converted_data = [
            tuple(float(x) if isinstance(x, (np.float64, np.float32)) else int(x) if isinstance(x, (np.int64, np.int32)) else x for x in row)
            for row in data
        ]
        cursor.executemany(sql, converted_data)
        conn.commit()
        print("📥 Options data stored successfully.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")

# === ANALYZE TREND ===
def analyze_trend_and_signal(prices, symbol, timestamps):
    directions = ["Up" if prices[i + 1] > prices[i] else "Down" for i in range(len(prices) - 1)]
    print(f"\n📈 Trend for {symbol}:")
    for i, direction in enumerate(directions):
        print(f"{timestamps[i]} {prices[i]} → {timestamps[i + 1]} {prices[i + 1]} | {direction}")
    signal = "BUY" if directions.count("Up") > directions.count("Down") else "SELL"
    print(f"Final Signal: {signal}")
    return signal

# === SAVE TRADE ===
def save_trade_to_db(activity_date, process_date, settle_date, instrument, description, tran_code, quantity, price, amount):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="123", database="hitman")
        cursor = conn.cursor()
        query = """
            INSERT INTO note (activity_date, process_date, settle_date, 
            instrument, description, tran_code, quantity, price, amount) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            activity_date.strftime('%Y-%m-%d %H:%M:%S'),
            process_date.strftime('%Y-%m-%d %H:%M:%S'),
            settle_date.strftime('%Y-%m-%d %H:%M:%S'),
            instrument, description, tran_code, quantity, price, amount
        )
        cursor.execute(query, values)
        conn.commit()
        print("✅ Trade saved to DB.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("❌ MySQL Insert Error:", err)

# === HOLDINGS ===
def get_stock_holding(symbol):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="123", database="hitman")
        cursor = conn.cursor()
        cursor.execute("SELECT tran_code, quantity FROM note WHERE instrument = %s", (symbol,))
        rows = cursor.fetchall()
        total_qty = sum(qty for tran_code, qty in rows if tran_code.upper() == 'BUY')
        cursor.close()
        conn.close()
        return total_qty
    except mysql.connector.Error as err:
        print("❌ MySQL Select Error:", err)
        return 0

# === PLACE TRADE ===
def place_ibkr_trade(symbol, description, signal, qty):
    print(f"[IBKR] Placing {signal} order for {symbol} ({qty} shares)")
    try:
        contract = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(contract)
        order = MarketOrder(signal, qty)
        trade = ib.placeOrder(contract, order)
        ib.sleep(1)
        if trade.orderStatus.status in ['Filled', 'Submitted']:
            activity_date = datetime.now()
            price = trade.fills[0].execution.price if trade.fills else 0
            print(f"✅ Filled Price: {price}")
            amount = price * qty
            print(f" Total Amount: ${amount:.2f}")
            save_trade_to_db(activity_date, activity_date, activity_date, symbol, description, signal, qty, price, amount)
        else:
            print("⚠️ Order not filled.")
    except Exception as e:
        print(f"❌ Trade error: {e}")

# === CHECK & TRADE ===
def check_and_trade(symbol, qty):
    holding = get_stock_holding(symbol)
    if holding == 0:
        print(f"✅ Buying {qty} of {symbol} (no current holdings)")
        place_ibkr_trade(symbol, symbol, "BUY", qty)
    else:
        print(f"⚠️ Already holding {holding} shares of {symbol}. Skipping buy.")

# === TREND BASED TRADING ===
def show_all_data_and_trade_ibkr():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="123", database="hitman")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT stock_symbol FROM options_trading")
        all_symbols = [row[0] for row in cursor.fetchall()]
        for sym in all_symbols:
            print(f"\n📊 {sym} (Today)")
            cursor.execute("""
                SELECT activity_date, stock_price FROM options_trading 
                WHERE stock_symbol = %s AND DATE(activity_date) = CURDATE()
                ORDER BY activity_date DESC LIMIT 6
            """, (sym,))
            rows = cursor.fetchall()
            if len(rows) < 2:
                print("❌ Not enough data.")
                continue
            rows.reverse()
            prices = [row[1] for row in rows]
            timestamps = [row[0] for row in rows]
            signal = analyze_trend_and_signal(prices, sym, timestamps)
            if signal == "BUY":
                check_and_trade(sym, 10)
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("❌ MySQL Error:", err)

# === MAIN LOOP ===
while True:
    now = datetime.now(eastern)
    if start_time <= now <= end_time:
        for sym in symbols:
            stock = yf.Ticker(sym)
            expiry_dates = stock.options
            if not expiry_dates:
                print(f"No option expiry dates available for {sym}.")
                continue
            expiry_date = expiry_dates[0]
            try:
                latest_price = stock.history(period="1d")['Close'].iloc[-1]
                opt_chain = stock.option_chain(expiry_date)
                calls, puts = opt_chain.calls, opt_chain.puts
                if calls.empty or puts.empty:
                    print(f"No options data available for {sym}.")
                    continue
                closest_call = calls.iloc[(calls['strike'] - latest_price).abs().argsort()[:1]]
                closest_put = puts.iloc[(puts['strike'] - latest_price).abs().argsort()[:1]]
                call_premium = (closest_call['bid'].values[0] + closest_call['ask'].values[0]) / 2
                put_premium = (closest_put['bid'].values[0] + closest_put['ask'].values[0]) / 2
                date_time = now.strftime('%Y-%m-%d %H:%M:%S')
                print(f"{date_time} | {sym} Price: ${latest_price:.2f} | Call: ${call_premium:.2f} | Put: ${put_premium:.2f}")
                store_data_in_db([(sym, latest_price, call_premium, put_premium)])
            except Exception as e:
                print(f"❌ Error fetching data for {sym}: {e}")
        time.sleep(120)
    else:
        print(f"⏰ Market window ended at {now.strftime('%H:%M:%S')} (US/Eastern). Starting trade check...")
        show_all_data_and_trade_ibkr()
        ib.disconnect()
        break
